from orders.models import Order, OrderItem
from rest_framework.response import Response
from orders.serializers import (
    OrderItemSerializer,
    OrderSerializer,
    UpdateCartSerializer,
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


class OrderViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    http_method_names = ["get", "post", "options"]
    permission_classes = [IsAuthenticated, CustomerAccessPermission]

    def list(self, request, *args, **kwargs):
        customer = request.user
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
