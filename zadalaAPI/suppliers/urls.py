from django.urls import path
from .views import SupplierRegisterView, SupplierLoginView


urlpatterns = [
    path('register', SupplierRegisterView.as_view()),
    path('login', SupplierLoginView.as_view())
]