from rest_framework import routers
from django.urls import path, include
from .views import ProductViewSet

# ProductDetailAPIView


router = routers.DefaultRouter(trailing_slash=False)
router.register("products", ProductViewSet, "products")
urlpatterns = router.urls

# urlpatterns = [
#     path('products', ProductViewSet.as_view()),
#     path('products/<str:id>', ProductDetailAPIView.as_view())
# ]
