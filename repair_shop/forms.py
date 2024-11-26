# repair_shop/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Customer
from django.forms import ModelForm
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

