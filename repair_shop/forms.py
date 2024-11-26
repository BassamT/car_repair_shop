# core/forms.py
from django import forms

class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField(label='Enter your email to access your account')
