import pytest
from django.contrib.auth.models import Group
from django.test.client import Client
from pytest_django.lazy_django import skip_if_no_django

from authentication.tests.factories.user_factory import UserFactory


@pytest.fixture
def logged_in_client(logged_in_user):
    user_token = logged_in_user.tokens().token
    return Client(HTTP_AUTHORIZATION=f"Bearer {user_token}")


@pytest.fixture
def logged_in_user():
    skip_if_no_django()
    return UserFactory.create(groups=Group.objects.all())


@pytest.fixture
def admin_group():
    UserFactory.create(groups=(Group.objects.filter(name="Admins")))
