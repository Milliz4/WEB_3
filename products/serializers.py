from rest_framework import serializers

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
)

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ['id', 'name', 'country', 'picture']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'category', 'manufacturer', 'name', 'price', 'stock', 'picture']


class ProductPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhoto
        fields = ['id', 'product', 'image']


class OrderSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        customer = attrs.get("customer", getattr(self.instance, "customer", None))
        address = attrs.get("address", getattr(self.instance, "address", None))

        if customer and address and address.customer_id != customer.id:
            raise serializers.ValidationError("Этот адрес принадлежит другому покупателю")

        return attrs

    class Meta:
        model = Order
        fields = ['id', 'customer', 'address', 'created_at', 'status']
        read_only_fields = ['created_at']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'price']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'customer', 'product', 'rating', 'text', 'created_at']
        read_only_fields = ['created_at']