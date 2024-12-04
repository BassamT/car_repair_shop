# repair_shop/urls.py

from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Home page
    path('', views.home, name='home'),

    # Services page
    path('services/', views.services, name='services'),

    # Employee login
    path('employee/login/', views.EmployeeLoginView.as_view(), name='employee_login'),

    # Customer access request
    path('customer/access/', views.customer_access_request, name='customer_access_request'),

    # Customer dashboard with token
    path('customer/access/<str:token>/', views.customer_dashboard, name='customer_dashboard'),

    path('contact/', views.contact, name='contact'),

    path('location/', views.location, name='location'),

     # Customer access request
    path('customer/access/', views.customer_access_request, name='customer_access_request'),

    # Customer dashboard with token
    path('customer/access/<str:token>/', views.customer_dashboard, name='customer_dashboard'),

    # Employee dashboard
    path('employee/dashboard/', views.employee_dashboard, name='employee_dashboard'),

    # Employee logout
    path('employee/logout/', LogoutView.as_view(next_page='home'), name='employee_logout'),

    path('employee/customers/add/', views.add_customer, name='add_customer'),

    path('employee/vehicles/add/', views.add_vehicle, name='add_vehicle'),

    path('employee/service-parts/add/', views.add_service_part, name='add_service_part'),

    path('employee/customers/', views.customer_list, name='customer_list'),

    # Password Reset URLs
    path('employee/password-reset/', auth_views.PasswordResetView.as_view(template_name='repair_shop/password_reset.html'), name='password_reset'),
    path('employee/password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='repair_shop/password_reset_done.html'), name='password_reset_done'),
    path('employee/password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='repair_shop/password_reset_confirm.html'), name='password_reset_confirm'),
    path('employee/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='repair_shop/password_reset_complete.html'), name='password_reset_complete'),

    # Invoice URLs
    path('employee/invoices/add/', views.add_invoice, name='add_invoice'),
    path('employee/invoices/<int:pk>/', views.invoice_detail, name='invoice_detail'),
    path('employee/invoices/', views.invoice_list, name='invoice_list'),

    # Vehicle List URL
    path('employee/vehicles/', views.vehicle_list, name='vehicle_list'),

    path('employee/service-parts/add/', views.add_service_part, name='add_service_part'),

    path('employee/service-parts/', views.service_part_list, name='service_part_list'),

    # Customer Dashboard
    path('customer/dashboard/<str:token>/', views.customer_dashboard, name='customer_dashboard'),
    path('customer/dashboard/<str:token>/appointment/', views.customer_dashboard, name='request_appointment'),
    path('customer/dashboard/<str:token>/support/', views.customer_dashboard, name='contact_support'),

    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    
    path('invoices/<int:pk>/', views.invoice_detail, name='invoice_detail'),

    path('vehicles/<uuid:token>/qr_code/download/', views.vehicle_qr_code_download, name='vehicle_qr_code_download'),
    path('vehicles/<uuid:token>/history/', views.vehicle_history, name='vehicle_history'),


    # Additional URL patterns for other views
    # Example:
    # path('contact/', views.contact, name='contact'),
]
