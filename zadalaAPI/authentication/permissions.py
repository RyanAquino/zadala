from django.contrib.auth.models import Group
from authentication.models import User
from rest_framework import permissions


class CustomerAccessPermission(permissions.BasePermission):
    group = "Customers"

    def has_permission(self, request, view):
        user_id = request.user.id
        return (
            Group.objects.get(name=self.group).user_set.filter(id=user_id).exists()
            or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        user_id = request.user.id
        return obj.id == user_id


class SupplierAccessPermission(permissions.BasePermission):
    group = "Suppliers"

    def has_permission(self, request, view):
        user_id = request.user.id
        return (
            Group.objects.get(name=self.group).user_set.filter(id=user_id).exists()
            or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        user_id = request.user.id
        return obj.id == user_id
