from rest_framework import serializers

from orders.models import Order, OrderItem, ShippingAddress
from products.serializers import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "customer",
            "date_ordered",
            "complete",
            "transaction_id",
            "get_cart_total",
            "get_cart_items",
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ["product", "order", "quantity", "date_added", "total"]


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = "__all__"
        read_only_fields = ("customer", "order")


class UpdateCartSerializer(serializers.Serializer):
    productId = serializers.IntegerField()
    action = serializers.CharField()
