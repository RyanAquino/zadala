from products.models import Product
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import ProductSerializer
from rest_framework_simplejwt.tokens import RefreshToken


from django.contrib.auth.models import Group
from rest_framework import permissions


class CustomerAccessPermission(permissions.BasePermission):
    group = 'Customers'

    def has_permission(self, request, view):
        user_id = request.user.id
        return Group.objects.get(name=self.group).user_set.filter(id=user_id).exists() or request.user.is_superuser


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [
        CustomerAccessPermission
    ]
    serializer_class = ProductSerializer

    @action(detail=True, methods=['POST'])
    def buy(self, request, pk=None):
        return Response({
            'status': 'triggered'
        })
