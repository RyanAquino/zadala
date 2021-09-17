from rest_framework.generics import get_object_or_404

from orders.exceptions import UnprocessableEntity
from orders.models import Order, OrderItem, ShippingAddress
from rest_framework.response import Response
from orders.serializers import (
    OrderItemSerializer,
    OrderSerializer,
    UpdateCartSerializer,
    ShippingAddressSerializer,
)
from rest_framework.permissions import IsAuthenticated
from authentication.permissions import (
    CustomerAccessPermission,
    SupplierAccessPermission,
)
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_condition import Or
from products.models import Product
import datetime


class OrderViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    http_method_names = ["get", "post", "options"]
    permission_classes = [IsAuthenticated, CustomerAccessPermission]

    def list(self, request, *args, **kwargs):
        customer = request.user
        self.check_object_permissions(self.request, customer)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.order_items
        serializer = OrderItemSerializer(items, many=True)

        resp = {
            "total_items": order.get_cart_items,
            "total_amount": order.get_cart_total,
            "products": sorted(
                serializer.data, key=lambda x: x["date_added"], reverse=True
            ),
        }

        return Response(resp)

    @action(
        detail=False,
        methods=["post"],
        url_path="update-cart",
        serializer_class=UpdateCartSerializer,
        permission_classes=[Or(CustomerAccessPermission, SupplierAccessPermission)],
    )
    def update_cart(self, request):
        request_data = self.get_serializer(data=request.data)
        request_data.is_valid(raise_exception=True)

        request_action = request_data.validated_data["action"]
        product_id = request_data.validated_data["productId"]
        customer = request.user
        self.check_object_permissions(self.request, customer)

        product = get_object_or_404(Product.objects.all(), pk=product_id)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        order_item, created = OrderItem.objects.get_or_create(
            order=order, product=product
        )

        if request_action == "add":
            order_item.quantity += 1
            if order_item.quantity > product.quantity:
                raise UnprocessableEntity(
                    detail="Order Item quantity exceeds available stock"
                )
        elif request_action == "remove":
            order_item.quantity -= 1

        order_item.save()

        if order_item.quantity <= 0:
            order_item.delete()

        items = order.order_items
        serializer = OrderItemSerializer(items, many=True)

        resp = {
            "total_items": order.get_cart_items,
            "total_amount": order.get_cart_total,
            "products": sorted(
                serializer.data, key=lambda x: x["date_added"], reverse=True
            ),
        }

        return Response(data=resp, status=200)

    @action(
        detail=False,
        methods=["post"],
        url_path="process-order",
        serializer_class=ShippingAddressSerializer,
        permission_classes=[Or(CustomerAccessPermission, SupplierAccessPermission)],
    )
    def process_order(self, request):
        request_data = self.get_serializer(data=request.data)
        transaction_id = datetime.datetime.now().timestamp()
        customer = request.user
        self.check_object_permissions(self.request, customer)

        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        request_data.is_valid(raise_exception=True)

        order.transaction_id = transaction_id
        order.complete = True
        order.save()

        if order.shipping:
            shipping = ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=request_data.data["address"],
                city=request_data.data["city"],
                state=request_data.data["state"],
                zipcode=request_data.data["zipcode"],
            )
            shipping.save()

            return Response(ShippingAddressSerializer(shipping).data, status=201)
        return Response("Order not found", status=400)
