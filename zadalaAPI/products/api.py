from products.models import Product
from rest_framework import viewsets, permissions
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = ProductSerializer
