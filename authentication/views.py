from rest_condition import Or
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from .permissions import CustomerAccessPermission, SupplierAccessPermission
from .serializers import (
    UserSerializer,
    UserLoginSerializers,
    SupplierSerializer,
    UserProfileSerializer,
)
from rest_framework.response import Response
from rest_framework import status


class UserRegisterView(GenericAPIView):
    serializer_class = UserSerializer
    authentication_classes: list = []
    permission_classes: list = []

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SupplierRegisterView(GenericAPIView):
    serializer_class = SupplierSerializer
    authentication_classes: list = []
    permission_classes: list = []

    def post(self, request):
        serializer = SupplierSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserLoginView(GenericAPIView):
    serializer_class = UserLoginSerializers
    authentication_classes: list = []
    permission_classes: list = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserProfileView(GenericAPIView):
    serializer_class = UserProfileSerializer
    pagination_class = None
    permission_classes = [
        IsAuthenticated,
        Or(SupplierAccessPermission, CustomerAccessPermission),
    ]

    def get(self, request):
        serializer = self.get_serializer(
            request.user,
            fields=(
                "id",
                "email",
                "first_name",
                "last_name",
                "last_login",
                "date_joined",
            ),
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        serializer = UserProfileSerializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.pop("password", None)
        if password:
            request.user.set_password(password)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
