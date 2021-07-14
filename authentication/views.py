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

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SupplierRegisterView(GenericAPIView):
    serializer_class = SupplierSerializer
    authentication_classes: list = []
    permission_classes: list = []

    def post(self, request):
        serializer = SupplierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
