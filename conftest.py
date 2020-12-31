import pytest
from authentication.tests.factories.user_factory import UserFactory
from django.test.client import Client
from pytest_django.lazy_django import skip_if_no_django
from authentication.tests.factories.group_factory import (
    CustomersGroupFactory,
    SuppliersGroupFactory,
    AdminsGroupFactory,
)


@pytest.fixture
def logged_in_client(logged_in_user):
    user_token = logged_in_user.tokens()["token"]
    return Client(HTTP_AUTHORIZATION=f"Bearer {user_token}")


@pytest.fixture
def logged_in_user():
    skip_if_no_django()

    user = UserFactory.create(
        groups=(
            CustomersGroupFactory.create(),
            SuppliersGroupFactory.create(),
            AdminsGroupFactory.create(),
        )
    )

    return user


@pytest.fixture
def admin_group():
    UserFactory.create(groups=(AdminsGroupFactory.create(),))
