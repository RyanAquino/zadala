from orders.models import Order, OrderItem
from products.models import Product
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import ProductSerializer
from authentication.permissions import (
    CustomerAccessPermission,
    SupplierAccessPermission,
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_condition import Or


class ProductViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, SupplierAccessPermission]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        """Sets the product supplier to the logged in user"""
        serializer.save(supplier=self.request.user)

    @action(
        detail=True,
        methods=["post"],
        url_path="add-to-cart",
        serializer_class=None,
        permission_classes=[Or(CustomerAccessPermission, SupplierAccessPermission)],
    )
    def add_to_cart(self, request, pk):
        customer = request.user
        product = Product.objects.get(id=pk)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        order_item, created = OrderItem.objects.get_or_create(
            order=order, product=product
        )
        order_item.quantity += 1
        order_item.save()

        return Response(status=200)
