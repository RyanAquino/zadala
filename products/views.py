from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from authentication.permissions import SupplierAccessPermission
from products.models import Product

from .serializers import ProductSerializer
from rest_framework.parsers import MultiPartParser
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from zadalaAPI.settings import CACHE_TTL
from django.core.cache import cache


class ProductViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, SupplierAccessPermission]
    queryset = Product.objects.all().order_by("created_at")
    serializer_class = ProductSerializer
    parser_classes = (MultiPartParser,)
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]

    def list(self, request, *args, **kwargs):
        cached_products = cache.get(f"products_{request.query_params}")

        if not cached_products:
            queryset = self.filter_queryset(self.get_queryset())
            cache.set(f"products_{request.query_params}", queryset, CACHE_TTL)
            page = self.paginate_queryset(queryset)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        page = self.paginate_queryset(cached_products)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    # @method_decorator(cache_page(CACHE_TTL, key_prefix="products"))
    # def dispatch(self, *args, **kwargs):
    #     return super(ProductViewSet, self).dispatch(*args, **kwargs)

    def perform_create(self, serializer):
        """Sets the product supplier to the logged in user"""
        serializer.save(supplier=self.request.user)

    def perform_destroy(self, instance):
        instance.image.delete()
        instance.delete()
