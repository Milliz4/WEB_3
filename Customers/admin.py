from django.contrib import admin
from customers.models import Customer, Group


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'group']

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
