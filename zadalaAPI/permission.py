from django.contrib.auth.models import Group
from rest_framework import permissions


class CustomerAccessPermission(permissions.BasePermission):
    message = 'Adding customers not allowed.'

    def has_permission(self, request, view):
        print(request)
        return True
        # try:
        #     return Group.objects.get(name=group_name).user_set.filter(id=user.id).exists()
        # except Group.DoesNotExist:
        #     return None

