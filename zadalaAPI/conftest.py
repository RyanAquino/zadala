import pytest
from authentication.factories.user_factory import UserFactory
from django.test.client import Client
from pytest_django.lazy_django import skip_if_no_django
from authentication.tests.base_data import base_data
from django.contrib.auth.models import Group


@pytest.fixture
def logged_in_client():
    skip_if_no_django()

    base_data()
    user = UserFactory()
    token = user.tokens()
    customers_group = Group.objects.get(name="Customers")
    suppliers_group = Group.objects.get(name="Suppliers")
    user.groups.add(customers_group)
    user.groups.add(suppliers_group)

    return Client(HTTP_AUTHORIZATION=f"Bearer {token['token']}")
