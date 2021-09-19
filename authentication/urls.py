from django.urls import path

from .views import (
    SupplierRegisterView,
    UserLoginView,
    UserProfileView,
    UserRegisterView,
    UserViewSet,
)

urlpatterns = [
    path("customer/register/", UserRegisterView.as_view()),
    path("supplier/register/", SupplierRegisterView.as_view()),
    path("login/", UserLoginView.as_view()),
    path("profile/", UserProfileView.as_view()),
    path("test/", UserViewSet.as_view({"get": "list"})),
]
