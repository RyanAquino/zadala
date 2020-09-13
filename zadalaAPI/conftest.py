import pytest
from authentication.factories.user_factory import UserFactory
from django.test.client import Client
from pytest_django.lazy_django import skip_if_no_django
from authentication.factories.group_factory import (
    CustomersGroupFactory,
    SuppliersGroupFactory,
)


@pytest.fixture
def logged_in_client(logged_in_user):
    user_token = logged_in_user.tokens()["token"]
    return Client(HTTP_AUTHORIZATION=f"Bearer {user_token}")


@pytest.fixture
def logged_in_user():
    skip_if_no_django()

    user = UserFactory.create(
        groups=(CustomersGroupFactory.create(), SuppliersGroupFactory.create())
    )

    return user