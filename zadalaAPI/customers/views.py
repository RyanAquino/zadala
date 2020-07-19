from rest_framework.generics import GenericAPIView
from .serializers import CustomerSerializer, CustomerLoginSerializers
from rest_framework.response import Response
from rest_framework import status


class CustomerRegisterView(GenericAPIView):
    serializer_class = CustomerSerializer

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerLoginView(GenericAPIView):
    serializer_class = CustomerLoginSerializers

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
