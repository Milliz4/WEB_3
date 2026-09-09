from django.contrib import admin

from Customers.models import Customers

# Register your models here.
@admin.register(Customers)
class CustomersAdmin(admin.ModelAdmin):
    list_display = ['name', 'group_name']
