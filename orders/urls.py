from django.urls import include, path
from rest_framework.routers import DefaultRouter

from orders.views import OrderViewSet

router = DefaultRouter()
router.register("", OrderViewSet)
urlpatterns = [path("", include(router.urls))]
