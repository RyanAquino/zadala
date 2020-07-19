from django.urls import path
from .views import CustomerRegisterView


urlpatterns = [
    path('register', CustomerRegisterView.as_view())
]