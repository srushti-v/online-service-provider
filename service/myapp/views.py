from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from myapp.models import Ratings,Payment,ProviderRegistration,OtpCode,UserLogin,UserRegistration,AddServices,ServiceBooking
from django.contrib.auth.hashers import check_password  # For password checking
from django.contrib.auth.hashers import make_password
import uuid
from datetime import datetime
import random
import string
import smtplib
from django.db.models import Sum





def index(request):
    data = Ratings.objects.all()
    return render(request, 'index.html', {
        'data': data,
        'stars': range(1, 6)
    })


def provider_view_a(request):
    data=ProviderRegistration.objects.all()
    return render(request,'provider_view_a.html',{'data':data})


def provider_del(request,pk):
    data=ProviderRegistration.objects.get(id=pk)
    data.delete()
    return redirect('provider_view_a')


def services_view_a(request):
    data=AddServices.objects.all()
    return render(request,'services_view_a.html',{'data':data})


def admin_home(request):
    return render(request,'admin_home.html')

def user_home(request):
    return render(request,'user_home.html')

def provider_home(request):
    return render(request,'provider_home.html')



def login(request):
    if request.method == "POST":
        uname = request.POST.get('t1')
        upass = request.POST.get('t2')
        try:
            udata = UserLogin.objects.get(username=uname)

            if check_password(upass, udata.password):  # Correct way to verify password
                request.session['username'] = uname

                if udata.utype == "admin":
                    messages.success(request, "Welcome Admin! You have successfully logged in.")
                    return redirect('admin_home')
                elif udata.utype == "user":
                    messages.success(request, "Welcome User! You have successfully logged in.")
                    return redirect('user_home')
                elif udata.utype == "provider":
                    messages.success(request, "Welcome Service Provider! You have successfully logged in.")
                    return redirect('provider_home')
            else:
                messages.error(request, "Invalid password.")
                return redirect('login')
                #return render(request, 'index.html', {'msg': 'Invalid password'})  # Password mismatch

        except UserLogin.DoesNotExist:
            messages.error(request, "Invalid password.")
            return redirect('login')
            #return render(request, 'index.html', {'msg': 'Invalid username'})  # User not found

    return render(request, 'login.html')



def register(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname', '').strip()
        lastname = request.POST.get('lastname', '').strip()
        city = request.POST.get('city', '').strip()
        pincode = request.POST.get('pincode', '').strip()
        address = request.POST.get('address', '').strip()
        mobile_no = request.POST.get('mobile_no', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        profile = request.FILES.get('file')

        # Debugging: Print received data
        print(f"Received Data:{firstname}, {lastname}, {email}, {password}")

        # 🔹 Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        # 🔹 Hash password
        hashed_password = make_password(password)

        # 🔹 Check if email already exists
        if UserRegistration.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('register')

        try:
            # 🔹 Save user in UserRegistration
            user = UserRegistration.objects.create(
                firstname=firstname, lastname=lastname,
                city=city, pincode=pincode, address=address,
                mobile_no=mobile_no, email=email, password=hashed_password,profile=profile
            )
            print("UserRegistration saved successfully!")  # Debugging

            # 🔹 Store credentials in UserLogin table
            UserLogin.objects.create(utype='user', username=email, password=hashed_password)
            print("UserLogin saved successfully!")  # Debugging

            messages.success(request, "Registration successful! You can now login.")
            return redirect('login')

        except Exception as e:
            print(f"Error occurred: {e}")  # Debugging
            messages.error(request, "An error occurred. Please try again.")

    return render(request, "reg.html")


def add_provider(request):
    if request.method == "POST":
        service_type = request.POST.get('service_type')
        firstname = request.POST.get('firstname', '').strip()
        lastname = request.POST.get('lastname', '').strip()
        city = request.POST.get('city', '').strip()
        pincode = request.POST.get('pincode', '').strip()
        address = request.POST.get('address', '').strip()
        mobile_no = request.POST.get('mobile_no', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        profile = request.FILES.get('file')

        # Debugging: Print received data
        print(f"Received Data:{firstname}, {lastname}, {email}, {password}")

        # 🔹 Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('add_provider')

        # 🔹 Hash password
        hashed_password = make_password(password)

        # 🔹 Check if email already exists
        if ProviderRegistration.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('add_provider')

        try:
            # 🔹 Save user in UserRegistration
            user = ProviderRegistration.objects.create(
                service_type=service_type,firstname=firstname, lastname=lastname,
                city=city, pincode=pincode, address=address,
                mobile_no=mobile_no, email=email, password=hashed_password,profile=profile
            )
            print("UserRegistration saved successfully!")  # Debugging

            # 🔹 Store credentials in UserLogin table
            UserLogin.objects.create(utype='provider', username=email, password=hashed_password)
            print("UserLogin saved successfully!")  # Debugging

            messages.success(request, "Registration successful! You can now login.")
            return redirect('admin_home')

        except Exception as e:
            print(f"Error occurred: {e}")  # Debugging
            messages.error(request, "An error occurred. Please try again.")

    return render(request, "add_provider.html")


def add_services(request):
    username = request.session['username']
    data=ProviderRegistration.objects.get(email=username)
    service_type=data.service_type
    if request.method == 'POST':
        service_name = request.POST.get('service_name')
        service_charge = request.POST.get('service_charge')
        per_hour_charge = request.POST.get('per_hour_charge') or None
        per_day_charge = request.POST.get('per_day_charge') or None

        AddServices.objects.create(
            provider_id=username,
            service_name=service_name,
            service_charge=service_charge,
            per_hour_charge=per_hour_charge,
            per_day_charge=per_day_charge
        )
        return redirect('services_view')  # Replace with your success URL

    return render(request, 'add_services.html',{'username':username,'service_type':service_type})


def services_view(request):
    uname = request.session['username']
    udata = AddServices.objects.filter(provider_id=uname).values()
    return render(request,'services_view.html',{'udata':udata})

def service_providers_u(request,service):
    data=ProviderRegistration.objects.filter(service_type=service).values()
    return render(request,'service_providers_u.html',{'data':data})

def service_del(request,pk):
    data=AddServices.objects.get(id=pk)
    data.delete()
    return redirect('services_view')

def book_service(request,pk):
    userid=request.session['username']
    data=ProviderRegistration.objects.get(id=pk)
    provider_id=data.email
    if request.method=="POST":
        service=request.POST.get('service_name')
        service_date = request.POST.get('service_date')
        schedule_time = request.POST.get('schedule_time')
        address = request.POST.get('address')
        description = request.POST.get('description')
        ServiceBooking.objects.create(charges=0,userid=userid,provider_id=provider_id,service=service,scheduled_date=service_date,scheduled_time=schedule_time,address=address,description=description)
        return render(request,'book_service.html',{'msg':'Booking request has sent successfully'})

    return render(request,'book_service.html')


def service_book_status(request):
    username = request.session['username']
    data=ServiceBooking.objects.filter(userid=username).values()
    return render(request,'service_book_status.html',{'udata':data})


def view_service_charges(request,email):
    data=AddServices.objects.filter(provider_id=email).values()
    return render(request,'view_service_charges.html',{'udata':data})





def service_request_user(request,serive):
    return render(request,'service_request_user.html')


def service_payment_user(request):
    userid=request.session['username']
    #data=ServiceBooking.objects.get(userid=userid)
    data = Payment.objects.filter(userid=userid).values()
    return render(request,'service_payment_user.html',{'data':data})

def service_payment_p(request):
    userid=request.session['username']
    data = Payment.objects.filter(provider_id=userid).values()
    return render(request,'service_payment_p.html',{'data':data})



def feedback(request):
    services = AddServices.objects.all()
    if request.method == "POST":
        service_name = request.POST.get('service_name')
        booking_id = request.POST.get('booking')
        customer_name = request.POST.get('customer_name')
        rating = request.POST.get('rating')
        review = request.POST.get('comments')

        # Get the actual service and booking model instances
        service = get_object_or_404(AddServices, service_name=service_name)
        bdata=ServiceBooking.objects.filter(id=booking_id).count()
        if bdata>=1:
            booking = get_object_or_404(ServiceBooking, id=int(booking_id))
            Ratings.objects.create(
                service=service,
                booking=booking,
                customer_name=customer_name,
                rating=int(rating),
                review=review
            )
            return render(request, 'feedback.html', {'msg': 'Thank you for your valid feedback', 'services': services})
        else:
            return render(request, 'feedback.html', {'msg': 'Invalid booking ID entered.','services': services})

    return render(request, 'feedback.html', {'services': services})



def service_requests_provider(request):
    username = request.session['username']
    data = ServiceBooking.objects.filter(provider_id=username).values()
    return render(request, 'service_requests_provider.html', {'udata': data})

def update_service_status(request,pk):
    if request.method=="POST":
        status = request.POST.get('status')
        charges = request.POST.get('charges')
        ServiceBooking.objects.filter(id=pk).update(status=status,charges=charges)
        messages.success(request,'Updated Successfully')
        return redirect('service_requests_provider')
    return render(request,'update_service_status.html')


def feedback_view_p(request):
    data = Ratings.objects.all()
    return render(request, 'feedback_view_p.html', {
        'data': data,
        'stars': range(1, 6)
    })

def feedback_view_a(request):
    data = Ratings.objects.all()
    return render(request, 'feedback_view_a.html', {
        'data': data,
        'stars': range(1, 6)
    })


def view_charges(request,charges,id):
    count=Payment.objects.filter(booking_id=id).filter(payment_status='paid').count()
    if charges==0:
        return render(request, 'message2.html')

    elif count>=1:
        return render(request,'message1.html')
    else:
        half_charges = int(charges / 2)
        return render(request,'view_charges.html',{'charges':charges,'c':half_charges,'id':id})


def make_payment(request, id, amount):
    userid = request.session.get('username')

    if request.method == "POST":
        # ✅ Generate transaction ID
        prefix = "TXN"
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        rand_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        transaction_id = f"{prefix}{timestamp}{rand_str}"

        # ✅ Get actual booking object instead of ID
        booking_obj = get_object_or_404(ServiceBooking, id=id)

        # ✅ Create Payment record
        Payment.objects.create(
            booking=booking_obj,
            amount_paid=amount,
            payment_status='paid',
            transaction_id=transaction_id,
            userid=userid
        )

        return render(request, 'message.html', {
            'transaction_id': transaction_id,
            'amount': amount
        })

    return render(request, 'make_payment.html', {'id': id, 'amount': amount})


def forgotpass(request):
    if request.method=="POST":
        username=request.POST.get('t1')
        request.session['username']=username
        ucheck=UserLogin.objects.filter(username=username).count()
        if ucheck>=1:
            otp=random.randint(1111,9999)
            OtpCode.objects.create(otp=otp,status='active')
            content = "Your OTP is - " + str(otp)
            mail=smtplib.SMTP('smtp.gmail.com',587)
            mail.ehlo()
            mail.starttls()
            mail.login('srushtivenkaraddi@gmail.com','mpic tjvu gibj fosw')
            mail.sendmail('srushtivenkaraddi@gmail.com',username,content)
            return redirect('otp')
        else:
            return render(request,'forgotpass.html',{'msg':"inalid username"})
    return render(request,'forgotpass.html')

def otp(request):
    if request.method=="POST":
        otp=request.POST.get('t1')
        ucheck=OtpCode.objects.filter(otp=otp).count()
        if ucheck>=1:
            return redirect('resetpass')
        else:
            return render(request,'otp.html',{'msg':'invalid otp'})
    return render(request,'otp.html')

def resetpass(request):
    username = request.session.get('username')  # safer than direct access
    if request.method == "POST":
        newpassword = request.POST.get('t1')
        confirmpassword = request.POST.get('t2')
        hashed_password = make_password(newpassword)
        if newpassword == confirmpassword:
            UserLogin.objects.filter(username=username).update(password=hashed_password)
            return redirect('login')
        else:
            return render(request, 'resetpass.html', {'msg': 'New password and confirm password must be the same.'})
    return render(request, 'resetpass.html')


def profile(request):
    username=request.session['username']
    data=UserRegistration.objects.filter(email=username).values()
    if request.method == "POST":
        firstname = request.POST.get('firstname', '').strip()
        lastname = request.POST.get('lastname', '').strip()
        pincode = request.POST.get('pincode', '').strip()
        address = request.POST.get('address', '').strip()
        mobile_no = request.POST.get('mobile_no', '').strip()

        if request.FILES.get('profile'):
            UserRegistration.objects.filter(email=username).update(
                firstname=firstname, lastname=lastname,
                 pincode=pincode, address=address,
                mobile_no=mobile_no,profile=profile
            )
            return redirect('profile')
        else:
            UserRegistration.objects.filter(email=username).update(
                    firstname=firstname, lastname=lastname,
                    pincode=pincode, address=address,
                    mobile_no=mobile_no
                )
            return redirect('profile')


    return render(request,'profile.html',{'data':data})




def report(request):
    data = Payment.objects.all()
    total_amount = Payment.objects.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    return render(request, 'report.html', {'data': data, 'total_amount': total_amount})