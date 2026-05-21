"""
URL configuration for service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('login',views.login,name='login'),
    path('register',views.register,name='register'),
    path('user_home',views.user_home,name='user_home'),
    path('admin_home',views.admin_home,name='admin_home'),
    path('provider_home',views.provider_home,name='provider_home'),
    path('add_services',views.add_services,name='add_services'),
    path('services_view',views.services_view,name='services_view'),
    path('service_request_user/<str:service>',views.service_request_user,name='service_request_user'),
    path('service_providers_u/<str:service>',views.service_providers_u,name='service_providers_u'),
    path('book_service/<int:pk>',views.book_service,name='book_service'),
    path('add_provider',views.add_provider,name='add_provider'),
    path('provider_view_a',views.provider_view_a,name='provider_view_a'),
    path('provider_del/<int:pk>',views.provider_del,name='provider_del'),
    path('service_del/<int:pk>',views.service_del,name='service_del'),
    path('services_view_a',views.services_view_a,name='services_view_a'),
    path('feedback_view_a',views.feedback_view_a,name='feedback_view_a'),
    path('view_service_charges/<str:email>',views.view_service_charges,name='view_service_charges'),
    path('service_book_status',views.service_book_status,name='service_book_status'),
    path('service_payment_user',views.service_payment_user,name='service_payment_user'),
    path('service_payment_p', views.service_payment_p, name='service_payment_p'),
    path('feedback',views.feedback,name='feedback'),
    path('feedback_view_p',views.feedback_view_p,name='feedback_view_p'),
    path('update_service_status/<int:pk>',views.update_service_status,name='update_service_status'),
    path('service_requests_provider',views.service_requests_provider,name='service_requests_provider'),
    path('view_charges/<int:charges>/<int:id>',views.view_charges,name='view_charges'),
    path('make_payment/<int:id>/<int:amount>',views.make_payment,name='make_payment'),
    path('forgotpass',views.forgotpass,name='forgotpass'),
    path('otp',views.otp,name='otp'),
    path('resetpass',views.resetpass,name='resetpass'),
    path('profile', views.profile, name='profile'),
    path('report',views.report,name='report'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
