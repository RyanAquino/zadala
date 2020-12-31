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
            "products": serializer.data,
        }

        return Response(resp)

    @action(
        detail=True,
        methods=["post"],
        url_path="update-cart",
        serializer_class=UpdateCartSerializer,
        permission_classes=[Or(CustomerAccessPermission, SupplierAccessPermission)],
    )
    def update_cart(self, request, pk):
        request_data = self.get_serializer(data=request.data)

        if request_data.is_valid():
            request_action = request_data.data["action"]
            product_id = request_data.data["productId"]
            customer = request.user
            self.check_object_permissions(self.request, customer)

            product = Product.objects.get(id=product_id)
            order, created = Order.objects.get_or_create(
                customer=customer, complete=False
            )

            order_item, created = OrderItem.objects.get_or_create(
                order=order, product=product
            )

            if request_action == "add":
                order_item.quantity += 1
            elif request_action == "remove":
                order_item.quantity -= 1

            order_item.save()

            if order_item.quantity <= 0:
                order_item.delete()

            return Response(status=200)

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

        if request_data.is_valid():
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
        return Response("Request data invalid", status=400)
