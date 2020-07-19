from products.models import Product
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductSerializer
from zadalaAPI.permissions import CustomerAccessPermission


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [
        IsAuthenticated,
        CustomerAccessPermission
    ]
    serializer_class = ProductSerializer
