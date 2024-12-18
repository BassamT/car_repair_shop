# repair_shop/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Customer, Invoice, InvoiceItem
from django.forms import ModelForm, inlineformset_factory
from .models import Vehicle
from .models import ServicePart


class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField(label='Enter your email to access your account')


class CustomerAccessForm(forms.Form):
    email = forms.EmailField(label='Enter your email address', max_length=254)


class EmployeeLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=254)


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'


class VehicleForm(ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'


class ServicePartForm(ModelForm):
    class Meta:
        model = ServicePart
        fields = '__all__'


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['customer', 'vehicle', 'notes']

InvoiceItemFormSet = inlineformset_factory(
    Invoice,
    InvoiceItem,
    fields=['service_part', 'quantity'],
    extra=1,
    can_delete=True,
    widgets={
        'quantity': forms.NumberInput(attrs={'min': '1'}),
    }
)


class ServicePartForm(forms.ModelForm):
    class Meta:
        model = ServicePart
        fields = ['name', 'description', 'unit_price']


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-dark text-white border-secondary',
            'placeholder': 'Your Name',
            'id': 'name',
        }),
        label='Name'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control bg-dark text-white border-secondary',
            'placeholder': 'Your Email',
            'id': 'email',
        }),
        label='Email'
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control bg-dark text-white border-secondary',
            'placeholder': 'Your Message',
            'rows': 5,
            'id': 'message',
        }),
        label='Message'
    )