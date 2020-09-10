from products.models import Product
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductSerializer
from authentication.permissions import (
    CustomerAccessPermission,
    SupplierAccessPermission,
)
from django.shortcuts import get_object_or_404
from rest_condition import Or


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [
        IsAuthenticated,
        Or(CustomerAccessPermission, SupplierAccessPermission),
    ]
    serializer_class = ProductSerializer


# class ProductViewSet(generics.ListAPIView, generics.CreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#
#
# class ProductDetailAPIView(generics.RetrieveAPIView,
#                            generics.DestroyAPIView,
#                            generics.UpdateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     lookup_field = 'id'
