from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from decimal import Decimal
import uuid

class ActivityLog(models.Model):
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp} - {self.description}"


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    address = models.TextField()
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Vehicle(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='vehicles')
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    vin = models.CharField(max_length=17, unique=True)
    license_plate = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.make} {self.model} ({self.license_plate})"


class ServicePart(models.Model):
    SERVICE = 'Service'
    PART = 'Part'
    TYPE_CHOICES = [
        (SERVICE, 'Service'),
        (PART, 'Part'),
    ]

    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    name = models.CharField(max_length=100)
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name




class Employee(AbstractUser):
    ROLE_CHOICES = [
        ('Administrator', 'Administrator'),
        ('Staff', 'Staff'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username


class Invoice(models.Model):
    PAID = 'Paid'
    UNPAID = 'Unpaid'
    PARTIALLY_PAID = 'Partially Paid'
    PAYMENT_STATUS_CHOICES = [
        (PAID, 'Paid'),
        (UNPAID, 'Unpaid'),
        (PARTIALLY_PAID, 'Partially Paid'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='invoices')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='invoices')
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    invoice_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    payment_status = models.CharField(max_length=15, choices=PAYMENT_STATUS_CHOICES, default=UNPAID)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Invoice #{self.id} - {self.customer}"

    def calculate_total(self):
        total = sum(item.total_price for item in self.items.all())
        self.total_amount = total
        self.save()

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    service_part = models.ForeignKey(ServicePart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.unit_price = self.service_part.unit_price
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)
        # Update the invoice total amount
        self.invoice.calculate_total()

    def __str__(self):
        return f"{self.service_part.name} x {self.quantity}"



class AccessToken(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='access_tokens')
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        # Token is valid for 1 hour
        return timezone.now() - self.created_at < timedelta(hours=1)

    def __str__(self):
        return f"AccessToken(token={self.token}, customer={self.customer.email})"


