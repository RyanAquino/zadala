from datetime import datetime
from uuid import uuid4

import django_rq
from drf_yasg.utils import swagger_auto_schema
from rest_condition import Or
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.permissions import (
    CustomerAccessPermission,
    SupplierAccessPermission,
)
from orders.exceptions import UnprocessableEntity
from orders.models import Order, OrderItem, ShippingAddress
from orders.serializers import (
    OrderSerializer,
    ShippingAddressSerializer,
    ShippingHistoryPaginatedSerializer,
    UpdateCartSerializer,
    UserOrderSerializer,
)
from orders.tasks import send_email_notification
from products.models import Product


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 1000

    def paginate(self, queryset, request):
        """
        Custom handler of paginating queryset
        :param queryset: Queryset
        :param request: Request object
        :return: Paginated response
        """
        res = self.paginate_queryset(queryset, request)
        return self.get_paginated_response(res)


class OrderViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    http_method_names = ["get", "post", "options"]
    pagination_class = None
    permission_classes = [
        IsAuthenticated,
        Or(CustomerAccessPermission, SupplierAccessPermission),
    ]

    @swagger_auto_schema(responses={200: UserOrderSerializer()})
    def list(self, request, *args, **kwargs):
        order, created = Order.objects.get_or_create(
            customer=request.user, complete=False
        )

        resp = {
            "total_items": order.get_cart_items,
            "total_amount": order.get_cart_total,
            "products": sorted(
                order.order_items, key=lambda item: item.date_added, reverse=True
            ),
        }

        return Response(data=UserOrderSerializer(instance=resp).data)

    @swagger_auto_schema(responses={200: ShippingHistoryPaginatedSerializer()})
    @action(
        detail=False,
        methods=["get"],
        url_path="history",
        serializer_class=ShippingHistoryPaginatedSerializer,
        pagination_class=StandardResultsSetPagination,
    )
    def order_history(self, request):
        paginator = self.pagination_class()
        completed_orders = Order.objects.filter(customer=request.user, complete=True)
        order_history = ShippingAddress.objects.filter(
            order__in=completed_orders
        ).order_by("-date_added")
        order_history = paginator.paginate(order_history, request)
        serializer = self.serializer_class(instance=order_history.data)
        return Response(data=serializer.data)

    @swagger_auto_schema(responses={201: UserOrderSerializer()})
    @action(
        detail=False,
        methods=["post"],
        url_path="update-cart",
        serializer_class=UpdateCartSerializer,
    )
    def update_cart(self, request):
        request_data = self.get_serializer(data=request.data)
        request_data.is_valid(raise_exception=True)

        request_action = request_data.validated_data["action"]
        product_id = request_data.validated_data["productId"]
        product = get_object_or_404(Product.objects.all(), pk=product_id)
        order, created = Order.objects.get_or_create(
            customer=request.user, complete=False
        )

        order_item, created = OrderItem.objects.get_or_create(
            order=order, product=product
        )

        if request_action == "add":
            order_item.quantity += 1
            if order_item.quantity > product.quantity:
                raise UnprocessableEntity(
                    detail="Order Item quantity exceeds available stock"
                )
        elif request_action == "remove":
            order_item.quantity -= 1

        order_item.save()

        if order_item.quantity <= 0:
            order_item.delete()

        resp = {
            "total_items": order.get_cart_items,
            "total_amount": order.get_cart_total,
            "products": sorted(
                order.order_items, key=lambda item: item.date_added, reverse=True
            ),
        }

        return Response(
            data=UserOrderSerializer(instance=resp).data, status=status.HTTP_201_CREATED
        )

    @action(
        detail=False,
        methods=["post"],
        url_path="process-order",
        serializer_class=ShippingAddressSerializer,
    )
    def process_order(self, request):
        request_data = self.get_serializer(data=request.data)
        transaction_id = str(uuid4())
        transaction_timestamp = datetime.now().strftime("%b %d, %Y %H:%M")
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        request_data.is_valid(raise_exception=True)

        order.transaction_id = transaction_id
        order.complete = True
        order.save()

        if not order.shipping:
            return Response("Order not found", status=status.HTTP_400_BAD_REQUEST)

        shipping = ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=request_data.validated_data["address"],
            city=request_data.validated_data["city"],
            state=request_data.validated_data["state"],
            zipcode=request_data.validated_data["zipcode"],
        )

        shipping.save()
        django_rq.enqueue(
            send_email_notification,
            customer.email,
            "invoice_email_template.html",
            f"Order Being Processed: {order.transaction_id}",
            {
                "user_first_name": customer.first_name,
                "user_last_name": customer.last_name,
                "shipping_address": shipping.address,
                "shipping_city": shipping.city,
                "shipping_state": shipping.state,
                "shipping_zipcode": shipping.zipcode,
                "invoice_code": transaction_id,
                "order_items": order.order_items,
                "order": order,
                "date_ordered": transaction_timestamp,
            },
        )

        return Response(
            ShippingAddressSerializer(shipping).data, status=status.HTTP_201_CREATED
        )
