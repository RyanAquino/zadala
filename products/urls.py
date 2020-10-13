from products.views import ProductViewSet
from rest_framework import routers
from django.urls import path, include


router = routers.DefaultRouter()
router.register("", ProductViewSet)
urlpatterns = [path("", include(router.urls))]
