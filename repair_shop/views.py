# repair_shop/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.contrib.auth.views import LoginView
from .forms import EmailAuthenticationForm, CustomerAccessForm
from .models import Customer, AccessToken, ServicePart, Invoice
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import uuid
from .forms import EmployeeLoginForm
from django.shortcuts import redirect
from .forms import CustomerForm
from .forms import VehicleForm
from .forms import ServicePartForm

# class EmployeeLoginView(LoginView):
#     template_name = 'repair_shop/employee_login.html'  # Updated template path

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Employee Login'
#         return context

def customer_access_request(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                customer = Customer.objects.get(email=email)
                token = get_random_string(32)
                AccessToken.objects.create(customer=customer, token=token)
                access_link = request.build_absolute_uri(f'/customer/access/{token}/')
                send_mail(
                    'Your Access Link',
                    f'Click the link to access your account: {access_link}',
                    'noreply@carrepairshop.com',
                    [email],
                )
                return render(request, 'repair_shop/access_sent.html')  # Updated template path
            except Customer.DoesNotExist:
                form.add_error('email', 'Email not found.')
    else:
        form = EmailAuthenticationForm()
    return render(request, 'repair_shop/customer_access.html', {'form': form})  # Updated template path

def customer_dashboard(request, token):
    try:
        access_token = AccessToken.objects.get(token=token)
        if access_token.is_valid():
            customer = access_token.customer
            invoices = customer.invoices.all()
            return render(request, 'repair_shop/customer_dashboard.html', {'customer': customer, 'invoices': invoices})  # Updated template path
        else:
            return render(request, 'repair_shop/access_expired.html')  # Updated template path
    except AccessToken.DoesNotExist:
        return render(request, 'repair_shop/invalid_token.html')  # Updated template path

def services(request):
    services = ServicePart.objects.filter(type='Service')
    return render(request, 'repair_shop/services.html', {'services': services})  # Updated template path

def invoice_detail(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    return render(request, 'repair_shop/invoice_detail.html', {'invoice': invoice})  # Updated template path

def home(request):
    return render(request, 'repair_shop/home.html')  # Added home view with correct template path

def contact(request):
    return render(request, 'repair_shop/contact.html')

def location(request):
    return render(request, 'repair_shop/location.html')


def customer_access_request(request):
    if request.method == 'POST':
        form = CustomerAccessForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                customer = Customer.objects.get(email=email)
                # Generate a unique token
                token_str = uuid.uuid4().hex
                token = AccessToken.objects.create(customer=customer, token=token_str)

                # Build the access link
                access_link = request.build_absolute_uri(
                    reverse('customer_dashboard', args=[token.token])
                )

                # Send email to customer
                subject = 'Your Access Link to Car Repair Shop'
                message = f"""
                Dear {customer.first_name},

                Click the link below to access your dashboard:
                {access_link}

                This link will expire in 1 hour.

                Best regards,
                Car Repair Shop Team
                """
                send_mail(
                    subject,
                    message,
                    None,  # Use DEFAULT_FROM_EMAIL
                    [customer.email],
                    fail_silently=False,
                )
                return render(request, 'repair_shop/access_email_sent.html', {'email': email})
            except Customer.DoesNotExist:
                form.add_error('email', 'No customer with this email found.')
    else:
        form = CustomerAccessForm()
    return render(request, 'repair_shop/customer_access_request.html', {'form': form})

# repair_shop/views.py



def customer_dashboard(request, token):
    access_token = get_object_or_404(AccessToken, token=token)
    if access_token.is_valid():
        customer = access_token.customer
        vehicles = customer.vehicles.all()
        invoices = customer.invoices.all()
        return render(request, 'repair_shop/customer_dashboard.html', {
            'customer': customer,
            'vehicles': vehicles,
            'invoices': invoices,
        })
    else:
        return render(request, 'repair_shop/token_expired.html')


class EmployeeLoginView(LoginView):
    template_name = 'repair_shop/employee_login.html'
    authentication_form = EmployeeLoginForm


@login_required
def employee_dashboard(request):
    return render(request, 'repair_shop/employee_dashboard.html')



@login_required
def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')  # Redirect to a customer list view
    else:
        form = CustomerForm()
    return render(request, 'repair_shop/add_customer.html', {'form': form})



@login_required
def add_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vehicle_list')  # Redirect to a vehicle list view
    else:
        form = VehicleForm()
    return render(request, 'repair_shop/add_vehicle.html', {'form': form})


@login_required
def add_service_part(request):
    if request.method == 'POST':
        form = ServicePartForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('service_part_list')  # Redirect to a service/part list view
    else:
        form = ServicePartForm()
    return render(request, 'repair_shop/add_service_part.html', {'form': form})


@login_required
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'repair_shop/customer_list.html', {'customers': customers})


@login_required
def employee_dashboard(request):
    return render(request, 'repair_shop/employee_dashboard.html')

