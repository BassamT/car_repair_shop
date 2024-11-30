# repair_shop/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail, BadHeaderError
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.contrib.auth.views import LoginView
from .forms import EmailAuthenticationForm, CustomerAccessForm
from .models import Customer, AccessToken, ServicePart, Invoice, Vehicle, ActivityLog
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import uuid
from .forms import EmployeeLoginForm
from django.shortcuts import redirect
from .forms import CustomerForm
from .forms import VehicleForm
from .forms import ServicePartForm
from .forms import InvoiceForm, InvoiceItemFormSet
from .forms import CustomerAccessForm
from .forms import ContactForm
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from datetime import timedelta
from django import forms



# class EmployeeLoginView(LoginView):
#     template_name = 'repair_shop/employee_login.html'  # Updated template path

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Employee Login'
#         return context

# Contact Form Definition
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control bg-dark text-white border-secondary',
        'placeholder': 'Your Name'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control bg-dark text-white border-secondary',
        'placeholder': 'Your Email'
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control bg-dark text-white border-secondary',
        'placeholder': 'Your Message',
        'rows': 5
    }))


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Extract form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message_content = form.cleaned_data['message']

            # Send email
            subject = f'Contact Message from {name}'
            message = f'Name: {name}\nEmail: {email}\n\nMessage:\n{message_content}'
            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_FROM_EMAIL])
                messages.success(request, 'Your message has been sent successfully!')
            except Exception as e:
                messages.error(request, f'Failed to send your message: {e}')
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'repair_shop/contact.html', {'form': form})



def services(request):
    services = ServicePart.objects.filter(type='Service')
    return render(request, 'repair_shop/services.html', {'services': services})  # Updated template path

def invoice_detail(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    return render(request, 'repair_shop/invoice_detail.html', {'invoice': invoice})  # Updated template path

def home(request):
    return render(request, 'repair_shop/home.html')  # Added home view with correct template path



def location(request):
    return render(request, 'repair_shop/location.html')

def customer_access_request(request):
    """
    Handles customer access requests by sending an access link via email.
    """
    if request.method == 'POST':
        form = CustomerAccessForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                customer = Customer.objects.get(email=email)
                
                # Generate a unique token using UUID4
                token = uuid.uuid4().hex
                
                # Create an AccessToken object
                AccessToken.objects.create(customer=customer, token=token)
                
                # Build the access link pointing to the customer_dashboard view with the token
                access_link = request.build_absolute_uri(
                    reverse('customer_dashboard', args=[token])
                )
                
                # Prepare email content
                subject = 'Your Access Link to Car Repair Shop'
                message = f"""
                Dear {customer.first_name},

                Click the link below to access your dashboard:
                {access_link}

                This link will expire in 1 hour.

                Best regards,
                Car Repair Shop Team
                """
                
                # Send the email
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,  # Ensure DEFAULT_FROM_EMAIL is set in settings.py
                    [customer.email],
                    fail_silently=False,
                )
                
                # Provide feedback to the user
                messages.success(request, f'Access link has been sent to {email}.')
                return render(request, 'repair_shop/access_email_sent.html', {'email': email})
            except Customer.DoesNotExist:
                form.add_error('email', 'No customer with this email found.')
    else:
        form = CustomerAccessForm()
    
    return render(request, 'repair_shop/customer_access_request.html', {'form': form})


def authenticate_customer(token):
    """
    Authenticates a customer using the provided token.
    Returns the Customer object if valid and not expired; otherwise, returns None.
    """
    try:
        access_token = AccessToken.objects.get(token=token)
        
        # Check if the token is still valid (e.g., valid for 1 hour)
        if access_token.is_valid():
            return access_token.customer
        else:
            # Optionally, delete expired tokens
            access_token.delete()
            return None
    except AccessToken.DoesNotExist:
        return None


def customer_dashboard(request, token):
    """
    Displays the customer dashboard if the provided token is valid.
    Handles appointment requests and support messages.
    """
    # Authenticate customer using the token
    customer = authenticate_customer(token)
    if not customer:
        messages.error(request, 'Invalid or expired access token. Please request a new access link.')
        return redirect('customer_access_request')

    # Fetch customer-related data
    vehicles = customer.vehicles.all()
    invoices = customer.invoices.all()

    if request.method == 'POST':
        if 'appointment_form' in request.POST:
            # Appointment Request Form Submission
            vehicle_id = request.POST.get('vehicle')
            preferred_date = request.POST.get('preferred_date')
            message_text = request.POST.get('message', '')
            try:
                vehicle = Vehicle.objects.get(id=vehicle_id, customer=customer)
            except Vehicle.DoesNotExist:
                messages.error(request, 'Selected vehicle does not exist.')
                return redirect('customer_dashboard', token=token)

            # Prepare email content
            subject = f"Appointment Request from {customer.first_name} {customer.last_name}"
            email_message = render_to_string('repair_shop/appointment_email.txt', {
                'customer': customer,
                'vehicle': vehicle,
                'preferred_date': preferred_date,
                'message': message_text,
            })

            # Send email
            send_mail(
                subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.SHOP_EMAIL],  # Ensure SHOP_EMAIL is set in settings.py
            )

            # Provide feedback to the user
            messages.success(request, 'Your appointment request has been submitted.')
            # Redirect to avoid resubmission
            return redirect('customer_dashboard', token=token)
        
        elif 'support_form' in request.POST:
            # Contact Support Form Submission
            subject_text = request.POST.get('subject')
            message_text = request.POST.get('message')
            if not subject_text or not message_text:
                messages.error(request, 'Please provide both a subject and a message.')
                return redirect('customer_dashboard', token=token)

            # Prepare email content
            email_subject = f"Support Message from {customer.first_name} {customer.last_name}: {subject_text}"
            email_message = render_to_string('repair_shop/support_email.txt', {
                'customer': customer,
                'message': message_text,
            })

            # Send email
            send_mail(
                email_subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.SHOP_EMAIL],
            )

            # Provide feedback to the user
            messages.success(request, 'Your message has been sent to our support team.')
            # Redirect to avoid resubmission
            return redirect('customer_dashboard', token=token)
    
    context = {
        'customer': customer,
        'vehicles': vehicles,
        'invoices': invoices,
        'token': token,
    }
    return render(request, 'repair_shop/customer_dashboard.html', context)




class EmployeeLoginView(LoginView):
    template_name = 'repair_shop/employee_login.html'
    authentication_form = EmployeeLoginForm




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
    total_customers = Customer.objects.count()
    total_vehicles = Vehicle.objects.count()
    total_invoices = Invoice.objects.count()
    total_service_parts = ServicePart.objects.count()
    recent_activities = ActivityLog.objects.order_by('-timestamp')[:5]

    context = {
        'total_customers': total_customers,
        'total_vehicles': total_vehicles,
        'total_invoices': total_invoices,
        'total_service_parts': total_service_parts,
        'recent_activities': recent_activities,
    }
    return render(request, 'repair_shop/employee_dashboard.html', context)


@login_required
def invoice_detail(request, pk):
    invoice = Invoice.objects.get(pk=pk)
    return render(request, 'repair_shop/invoice_detail.html', {'invoice': invoice})


@login_required
def invoice_list(request):
    invoices = Invoice.objects.order_by('-invoice_date')
    return render(request, 'repair_shop/invoice_list.html', {'invoices': invoices})


@login_required
def add_invoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        formset = InvoiceItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            invoice = form.save(commit=False)
            invoice.employee = request.user
            invoice.save()
            formset.instance = invoice
            formset.save()
            invoice.calculate_total()

            # Log the activity
            ActivityLog.objects.create(
                employee=request.user,
                description=f"Created Invoice #{invoice.id} for {invoice.customer}"
            )

            return redirect('invoice_detail', pk=invoice.id)
    else:
        form = InvoiceForm()
        formset = InvoiceItemFormSet(request.POST or None, prefix='items')
    return render(request, 'repair_shop/add_invoice.html', {'form': form, 'formset': formset})

@login_required
def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'repair_shop/vehicle_list.html', {'vehicles': vehicles})


@login_required
def add_service_part(request):
    if request.method == 'POST':
        form = ServicePartForm(request.POST)
        if form.is_valid():
            service_part = form.save()
            # Log the activity
            ActivityLog.objects.create(
                employee=request.user,
                description=f"Added new service/part: {service_part.name}"
            )
            return redirect('service_part_list')  # Redirect to a list of service parts
    else:
        form = ServicePartForm()
    return render(request, 'repair_shop/add_service_part.html', {'form': form})


@login_required
def service_part_list(request):
    service_parts = ServicePart.objects.all()
    return render(request, 'repair_shop/service_part_list.html', {'service_parts': service_parts})
