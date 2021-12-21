from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from authentication.permissions import SupplierAccessPermission
from products.models import Product

from .serializers import ProductSerializer


class ProductViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, SupplierAccessPermission]
    queryset = Product.objects.all().order_by("created_at")
    serializer_class = ProductSerializer
    parser_classes = (MultiPartParser,)
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]

    def perform_create(self, serializer):
        """Sets the product supplier to the logged in user"""
        serializer.save(supplier=self.request.user)

    def perform_destroy(self, instance):
        instance.image.delete()
        instance.delete()
