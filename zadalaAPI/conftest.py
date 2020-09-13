import pytest
from authentication.factories.user_factory import UserFactory
from django.test.client import Client
from pytest_django.lazy_django import skip_if_no_django
from authentication.factories.group_factory import (
    CustomersGroupFactory,
    SuppliersGroupFactory,
)


@pytest.fixture
def logged_in_client():
    skip_if_no_django()

    user = UserFactory.create(
        groups=(CustomersGroupFactory.create(), SuppliersGroupFactory.create())
    )
    token = user.tokens()

    return Client(HTTP_AUTHORIZATION=f"Bearer {token['token']}")
