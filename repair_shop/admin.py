from django.contrib import admin

from django.contrib import admin
from .models import Customer, Vehicle, ServicePart, Invoice, InvoiceItem

admin.site.register(Customer)
admin.site.register(Vehicle)
admin.site.register(ServicePart)
admin.site.register(Invoice)
admin.site.register(InvoiceItem)
