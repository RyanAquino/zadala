from authentication.tests.factories.user_factory import UserFactory
from authentication.models import User
import pytest


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
def test_user_login(client):
    """
    Test User login
    """
    user = UserFactory()
    data = {"email": user.email, "password": "password"}

    response = client.post("/v1/auth/login/", data)
    response_data = response.json()

    assert (
        response_data["email"] == "user3@email.com" and str(user) == "user3@email.com"
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_invalid_credentials_user_login(client):
    """
    Test Failed User login
    """
    data = {"email": "ryan@admin.com", "password": "password"}

    response = client.post("/v1/auth/login/", data)
    assert response.status_code == 403
    assert response.json() == {"detail": "Invalid email/password"}


@pytest.mark.django_db
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
