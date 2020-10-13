from orders.models import Order
from rest_framework.response import Response
from orders.serializers import OrderItemSerializer
from rest_framework.permissions import IsAuthenticated
from authentication.permissions import CustomerAccessPermission
from rest_framework.views import APIView
from orders.serializers import OrderSerializer


class OrderViewSet(APIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, CustomerAccessPermission]

    def get(self, request):
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.order_items
        serializer = OrderItemSerializer(items, many=True)

        resp = {
            "total_items": order.get_cart_items,
            "total_amount": order.get_cart_total,
            "products": serializer.data,
        }

        return Response(resp)
