# repair_shop/urls.py

from django.urls import path
from . import views

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

    # Additional URL patterns for other views
    # Example:
    # path('contact/', views.contact, name='contact'),
]
