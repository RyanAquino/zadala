from django.urls import path
from .views import SupplierRegisterView


urlpatterns = [
    path('register', SupplierRegisterView.as_view())
]