from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.validators import RegexValidator
from django.utils import timezone


class UserLogin(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)  # Store hashed passwords
    utype = models.CharField(max_length=10)

    def save(self, *args, **kwargs):
        # Hash password only if it's not already hashed
        if not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super(UserLogin, self).save(*args, **kwargs)



class UserRegistration(models.Model):
    firstname = models.CharField(max_length=100,null=True,blank=True)
    lastname = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    profile = models.ImageField(upload_to='images/',null=True,blank=True)
    pincode = models.CharField(max_length=6,null=True,blank=True,validators=[
        RegexValidator(r'^\d{6}$', message="Enter a valid 6-digit pincode")
    ])
    address = models.TextField(null=True,blank=True)

    mobile_no = models.CharField(max_length=10, unique=True,null=True,blank=True, validators=[
        RegexValidator(r'^\d{10}$', message="Enter a valid 10-digit mobile number")
    ])

    email = models.EmailField(unique=True,null=True,blank=True)
    password = models.CharField(max_length=255,null=True,blank=True)  # Store hashed password
    def save(self, *args, **kwargs):
        """ Hash password before saving """
        if not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super(UserRegistration, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.firstname} {self.lastname} ({self.utype})"



class ProviderRegistration(models.Model):

    service_type = models.CharField(max_length=100,null=True,blank=True)
    firstname = models.CharField(max_length=100,null=True,blank=True)
    lastname = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    profile = models.ImageField(upload_to='images/',null=True,blank=True)
    pincode = models.CharField(max_length=6,null=True,blank=True,validators=[
        RegexValidator(r'^\d{6}$', message="Enter a valid 6-digit pincode")
    ])
    address = models.TextField(null=True,blank=True)

    mobile_no = models.CharField(max_length=10, unique=True,null=True,blank=True, validators=[
        RegexValidator(r'^\d{10}$', message="Enter a valid 10-digit mobile number")
    ])

    email = models.EmailField(unique=True,null=True,blank=True)
    password = models.CharField(max_length=255,null=True,blank=True)  # Store hashed password
    def save(self, *args, **kwargs):
        """ Hash password before saving """
        if not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super(ProviderRegistration, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.firstname} {self.lastname})"



class AddServices(models.Model):
    SERVICE_CHOICES = [
        ('electrician', 'Electrician'),
        ('plumber', 'Plumber'),
        ('laundry', 'Laundry'),
        ('crane', 'Crane'),
    ]

    provider_id = models.CharField(max_length=100)
    service_name = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    service_charge = models.IntegerField()  # base/default charge
    per_hour_charge = models.IntegerField(null=True, blank=True)
    per_day_charge = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.get_service_name_display()} - ₹{self.service_charge}"





class ServiceBooking(models.Model):
    userid = models.CharField(max_length=100, null=True)
    provider_id = models.CharField(max_length=100, null=True)
    service = models.CharField(max_length=100,null=True)
    booking_date = models.DateTimeField(default=timezone.now,null=True)
    scheduled_date = models.DateField(null=True)
    scheduled_time = models.CharField(max_length=100, null=True)
    address = models.TextField(null=True)
    description = models.TextField(null=True)
    charges = models.PositiveIntegerField(null=True, blank=True)
    status_choices = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=status_choices,default='pending')

    def calculate_total_charge(self):
        if self.no_of_days and self.service.per_day_charge:
            return self.no_of_days * self.service.per_day_charge
        elif self.no_of_hours and self.service.per_hour_charge:
            return self.no_of_hours * self.service.per_hour_charge
        else:
            return self.service.service_charge

    def __str__(self):
        return f"{self.service.service_name} booking on {self.scheduled_date}"






class Payment(models.Model):
    booking = models.ForeignKey('ServiceBooking', on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status_choices = [
        ('success', 'Success'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
        ('paid', 'Paid'),
    ]
    payment_status = models.CharField(max_length=20, choices=payment_status_choices, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    userid = models.CharField(max_length=100, blank=True, null=True)
    provider_id = models.CharField(max_length=100, blank=True, null=True)
    payment_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.booking.id} - ₹{self.amount_paid} [{self.payment_status}]"



class Ratings(models.Model):
    service = models.ForeignKey('AddServices', on_delete=models.CASCADE)
    booking = models.ForeignKey('ServiceBooking', on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    rating = models.IntegerField()
    review = models.TextField(blank=True, null=True)
    rated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.customer_name} rated {self.service.service_name} - {self.rating}★"


class OtpCode(models.Model):
    otp=models.IntegerField()
    status=models.CharField(max_length=100)