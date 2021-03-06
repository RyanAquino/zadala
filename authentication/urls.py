from django.urls import path
from .views import UserRegisterView, UserLoginView, SupplierRegisterView


urlpatterns = [
    path("customer/register/", UserRegisterView.as_view()),
    path("supplier/register/", SupplierRegisterView.as_view()),
    path("login/", UserLoginView.as_view()),
]
