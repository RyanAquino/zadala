from rest_framework.generics import GenericAPIView
from .serializers import SupplierSerializer
from rest_framework.response import Response
from rest_framework import status


class SupplierRegisterView(GenericAPIView):
    serializer_class = SupplierSerializer

    def post(self, request):
        serializer = SupplierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
