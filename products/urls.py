from products.views import ProductViewSet
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)
router.register("products", ProductViewSet, "products")
urlpatterns = router.urls
