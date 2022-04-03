from datetime import datetime
from unittest.mock import patch

import pytest
from django.contrib.auth.models import Group
from django.test import Client
from django.test.client import MULTIPART_CONTENT

from authentication.models import User
from authentication.tests.factories.user_factory import UserFactory


@pytest.mark.django_db
def test_create_superuser_command(admin_group):
    """
    Test admin account creation
    """
    admin = User.objects.create_superuser(
        "test@admin.com", "admin", "account", "password"
    )

    assert admin.get_username() == "test@admin.com"
    assert admin.first_name == "admin"
    assert admin.last_name == "account"
    assert admin.check_password("password")


@pytest.mark.django_db
def test_customer_register(logged_in_client):
    """
    Test Customer registration
    """
    data = {
        "password": "password",
        "email": "customer@example.com",
        "first_name": "customer",
        "last_name": "account",
    }

    response = logged_in_client.post("/v1/auth/customer/register/", data, format="json")

    assert response.status_code == 201

    response = logged_in_client.post("/v1/auth/customer/register/", data, format="json")

    assert response.status_code == 400
    assert response.json() == {"email": ["Email already in use"]}


@pytest.mark.django_db
def test_supplier_register(logged_in_client):
    """
    Test Supplier registration
    """
    data = {
        "password": "password",
        "email": "supplier@example.com",
        "first_name": "supplier",
        "last_name": "account",
    }

    response = logged_in_client.post("/v1/auth/supplier/register/", data, format="json")

    assert response.status_code == 201

    response = logged_in_client.post("/v1/auth/supplier/register/", data, format="json")

    assert response.status_code == 400
    assert response.json() == {"email": ["Email already in use"]}


@pytest.mark.django_db
def test_user_login_with_google_provider(client):
    """
    Test User login with email on existing OAuth user
    """
    user = UserFactory(
        email="test@email.com", password="temp-password", auth_provider="google"
    )
    data = {"email": user.email, "password": "temp-password"}

    response = client.post("/v1/auth/login/", data)
    response_data = response.json()

    assert response.status_code == 403
    assert response_data == {"detail": "Please login using your login provider."}


@pytest.mark.django_db
@patch("botocore.client.BaseClient._make_api_call", lambda *args, **kwargs: None)
def test_user_login(client):
    """
    Test User login
    """
    user = UserFactory(email="test@email.com")
    data = {"email": user.email, "password": "password"}

    response = client.post("/v1/auth/login/", data)
    response_data = response.json()

    assert response_data["email"] == "test@email.com" and str(user) == "test@email.com"
    assert response.status_code == 200


@pytest.mark.django_db
@patch("botocore.client.BaseClient._make_api_call", lambda *args, **kwargs: None)
def test_invalid_email_credentials_user_login(client):
    """
    Test Failed User login
    """
    data = {"email": "ryan@admin.com", "password": "password"}

    response = client.post("/v1/auth/login/", data)
    assert response.status_code == 403
    assert response.json() == {"detail": "Invalid email/password"}


@pytest.mark.django_db
@patch("botocore.client.BaseClient._make_api_call", lambda *args, **kwargs: None)
def test_invalid_password_credentials_user_login(client):
    """
    Test Failed User login
    """
    user = UserFactory()
    data = {"email": user.email, "password": "wrong-password"}

    response = client.post("/v1/auth/login/", data)
    assert response.status_code == 403
    assert response.json() == {"detail": "Invalid email/password"}


@pytest.mark.django_db
@patch("botocore.client.BaseClient._make_api_call", lambda *args, **kwargs: None)
def test_tokens(logged_in_client):
    """
    Test refresh token
    """
    user = UserFactory()
    data = {"email": user.email, "password": "password"}

    response = logged_in_client.post("/v1/auth/login/", data, format="json")
    data = response.json()

    assert data["refresh"] and data["access"]

    refresh_token = {"refresh": data["refresh"]}

    response = logged_in_client.post(
        "/v1/auth/token/refresh/", refresh_token, format="json"
    )

    assert response.status_code == 200
    assert response.json()["access"]


@pytest.mark.django_db
@patch("botocore.client.BaseClient._make_api_call", lambda *args, **kwargs: None)
def test_refresh_token_with_access_token(logged_in_client):
    """
    Test refresh token with access token should fail
    """
    user = UserFactory()
    data = {"email": user.email, "password": "password"}

    response = logged_in_client.post("/v1/auth/login/", data, format="json")
    data = response.json()
    refresh_token = {"refresh": data["access"]}
    response = logged_in_client.post(
        "/v1/auth/token/refresh/", refresh_token, format="json"
    )

    assert response.status_code == 401


@pytest.mark.django_db
def test_retrieve_user_profile():
    """
    Test retrieval of user profile
    """
    mock_logged_in_user = UserFactory(
        email="test_test2@email.com", first_name="test", last_name="test2"
    )
    user_token = mock_logged_in_user.tokens().token
    client = Client(HTTP_AUTHORIZATION=f"Bearer {user_token}")
    response = client.get("/v1/auth/profile/")
    data = response.json()

    assert response.status_code == 200
    assert data["first_name"] == "test"
    assert data["last_name"] == "test2"
    assert data["email"] == "test_test2@email.com"
    assert data["auth_provider"] == "email"
    assert data.get("password") is None


@pytest.mark.django_db
def test_patch_profile_details():
    """
    Test patch user profile
    """
    content_type = MULTIPART_CONTENT
    mock_logged_in_user = UserFactory(
        email="test_test2@email.com",
        first_name="test",
        last_name="test2",
        groups=Group.objects.all(),
    )
    user_token = mock_logged_in_user.tokens().token
    client = Client(HTTP_AUTHORIZATION=f"Bearer {user_token}")
    modified_data = {
        "first_name": "modified_name1",
        "last_name": "modified_name2",
        "password": "string123",
    }

    data = client._encode_json({} if not modified_data else modified_data, content_type)
    encoded_data = client._encode_data(data, content_type)
    response = client.generic(
        "PATCH",
        "/v1/auth/profile/",
        encoded_data,
        content_type=content_type,
        secure=False,
        enctype="multipart/form-data",
    )

    modified_user = User.objects.first()

    assert response.status_code == 204
    assert modified_user.first_name == "modified_name1"
    assert modified_user.last_name == "modified_name2"
    assert modified_user.check_password("string123") is True


@pytest.mark.django_db
def test_patch_profile_password_of_oauth_user_should_not_update():
    """
    Test patch user profile password of an existing oauth user should not update the password
    """
    content_type = MULTIPART_CONTENT
    mock_logged_in_user = UserFactory(
        email="test_test2@email.com",
        first_name="test",
        last_name="test2",
        auth_provider="google",
        password="oauth-generated-password",
        groups=Group.objects.all(),
    )
    user_token = mock_logged_in_user.tokens().token
    client = Client(HTTP_AUTHORIZATION=f"Bearer {user_token}")
    modified_data = {
        "password": "oauth-modified-password",
    }

    data = client._encode_json({} if not modified_data else modified_data, content_type)
    encoded_data = client._encode_data(data, content_type)
    response = client.generic(
        "PATCH",
        "/v1/auth/profile/",
        encoded_data,
        content_type=content_type,
        secure=False,
        enctype="multipart/form-data",
    )

    modified_user = User.objects.first()

    assert response.status_code == 204
    assert modified_user.check_password("oauth-generated-password") is True


@pytest.mark.django_db
@patch("botocore.client.BaseClient._make_api_call", lambda *args, **kwargs: None)
def test_login_should_update_last_login_date_time(client):
    """
    Test User login should update last login date time
    """
    user = UserFactory(last_login="2022-02-21 00:53:12.279437")
    data = {"email": user.email, "password": "password"}

    response = client.post("/v1/auth/login/", data)
    current_login_time = datetime.today().replace(microsecond=0).timestamp()

    assert response.status_code == 200
    user.refresh_from_db()

    user_last_login_second_timestamp = (
        User.objects.first().last_login.replace(microsecond=0).timestamp()
    )
    assert user_last_login_second_timestamp == current_login_time
