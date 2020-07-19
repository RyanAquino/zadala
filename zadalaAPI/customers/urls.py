from django.urls import path
from .views import CustomerRegisterView, CustomerLoginView


urlpatterns = [
    path('register', CustomerRegisterView.as_view()),
    path('login', CustomerLoginView.as_view())
]