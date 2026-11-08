from django.contrib import admin

from products.models import (
    Customer,
    Address,
    Category,
    Manufacturer,
    Product,
    ProductPhoto,
    Order,
    OrderItem,
    Review,
    Profile,
)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'email', 'phone']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'street', 'city', 'postal_code']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'country', 'picture']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'manufacturer', 'name', 'price', 'stock', 'picture']


@admin.register(ProductPhoto)
class ProductPhotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'image']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'address', 'created_at', 'status']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity', 'price']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'product', 'rating', 'text', 'created_at']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False