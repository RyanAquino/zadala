from authentication.tests.factories.user_factory import UserFactory
import pytest


@pytest.mark.django_db
def test_user_register(logged_in_client):
    """
    Test User registration
    """
    data = {
        "password": "password",
        "email": "customer@example.com",
        "first_name": "customer",
        "last_name": "account",
    }

    response = logged_in_client.post("/v1/auth/customer/register/", data, format="json")

    assert response.status_code == 201


@pytest.mark.django_db
def test_user_login(client):
    """
    Test User login
    """
    user = UserFactory()
    data = {"email": user.email, "password": "password"}

    response = client.post("/v1/auth/login/", data)
    response_data = response.json()

    assert response_data["email"] == "user1@email.com"
    assert response.status_code == 200


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
