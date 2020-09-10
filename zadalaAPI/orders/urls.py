from orders.views import OrderViewSet
from django.urls import path

urlpatterns = [
    path('orders', OrderViewSet.as_view()),
    # path('orders/<str:id>', ProductDetailAPIView.as_view())
]