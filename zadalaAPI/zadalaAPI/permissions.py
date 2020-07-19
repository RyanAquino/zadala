from django.contrib.auth.models import Group
from customers.models import Customer
from rest_framework import permissions


class CustomerAccessPermission(permissions.BasePermission):
    group = 'Customers'

    def has_permission(self, request, view):
        user_id = request.user.id

        print(Customer.objects.get(email=request.user.email).groups.all())
        print(request.user)
        return Group.objects.get(name=self.group).user_set.filter(id=user_id).exists() or request.user.is_superuser


class SupplierAccessPermission(permissions.BasePermission):
    group = 'Suppliers'

    def has_permission(self, request, view):
        user_id = request.user.id
        return Group.objects.get(name=self.group).user_set.filter(id=user_id).exists() or request.user.is_superuser
