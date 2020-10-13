# from orders.views import OrderViewSet
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
#
#
# router = DefaultRouter()
# router.register("", OrderViewSet)
# urlpatterns = [path("", include(router.urls))]

from orders.views import OrderViewSet
from django.urls import path

urlpatterns = [
    path("", OrderViewSet.as_view()),
]
