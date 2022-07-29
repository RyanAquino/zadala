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


class OrderHistorySerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["date_ordered", "transaction_id", "order_items"]


class UserOrderSerializer(serializers.Serializer):
    total_items = serializers.IntegerField()
    total_amount = serializers.FloatField()
    products = OrderItemSerializer(many=True)


class ShippingHistorySerializer(serializers.ModelSerializer):
    order = OrderHistorySerializer()

    class Meta:
        model = ShippingAddress
        fields = ["order", "address", "state", "city", "zipcode", "date_added"]


class ShippingHistoryPaginatedSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField()
    previous = serializers.CharField()
    results = ShippingHistorySerializer(many=True)

    class Meta:
        fields = "__all__"


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = "__all__"
        read_only_fields = ("customer", "order")


class UpdateCartSerializer(serializers.Serializer):
    productId = serializers.IntegerField()
    action = serializers.CharField()
