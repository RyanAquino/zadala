from rest_framework import routers
from .api.api import ProductViewSet


router = routers.DefaultRouter(trailing_slash=False)
router.register('api/products', ProductViewSet, 'products')
urlpatterns = router.urls
