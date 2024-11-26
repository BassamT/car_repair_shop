# repair_shop/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.contrib.auth.views import LoginView
from .forms import EmailAuthenticationForm
from .models import Customer, AccessToken, ServicePart, Invoice
from django.contrib.auth.decorators import login_required

class EmployeeLoginView(LoginView):
    template_name = 'repair_shop/employee_login.html'  # Updated template path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Employee Login'
        return context

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