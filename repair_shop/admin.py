from django.contrib import admin

from django.contrib import admin
from .models import Customer, Vehicle, ServicePart, Invoice, InvoiceItem, Employee
from django.contrib.auth.admin import UserAdmin

class EmployeeAdmin(UserAdmin):
    model = Employee
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Customer)
admin.site.register(Vehicle)
admin.site.register(ServicePart)
admin.site.register(Invoice)
admin.site.register(InvoiceItem)
