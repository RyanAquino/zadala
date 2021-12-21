from django.urls import include, path
from rest_framework import routers

from products.views import ProductViewSet

router = routers.DefaultRouter()
router.register("", ProductViewSet)
urlpatterns = [path("", include(router.urls))]
