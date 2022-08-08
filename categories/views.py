from rest_framework.viewsets import ModelViewSet

from authentication.permissions import AdminAccessPermission
from categories.models import Category
from categories.serializers import CategorySerializer


class CategoryViewSet(ModelViewSet):
    permission_classes = [AdminAccessPermission]
    queryset = Category.objects.all().order_by("id")
    serializer_class = CategorySerializer
