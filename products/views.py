from products.models import Product
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import ProductSerializer
from authentication.permissions import SupplierAccessPermission
from rest_framework.viewsets import ModelViewSet


class ProductViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, SupplierAccessPermission]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        """Sets the product supplier to the logged in user"""
        serializer.save(supplier=self.request.user)
