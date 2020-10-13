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
def test_user_login(logged_in_client):
    """
    Test User login
    """
    data = {"email": "user@email.com", "password": "password"}

    response = logged_in_client.post("/v1/auth/login/", data, format="json")
    response_data = response.json()

    assert (data["email"] == response_data["email"]) and response_data
    assert response.status_code == 200


@pytest.mark.django_db
def test_tokens(logged_in_client):
    """
    Test refresh token
    """
    data = {"email": "user@email.com", "password": "password"}

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
    data = {"email": "user@email.com", "password": "password"}

    response = logged_in_client.post("/v1/auth/login/", data, format="json")
    data = response.json()
    refresh_token = {"refresh": data["access"]}
    response = logged_in_client.post(
        "/v1/auth/token/refresh/", refresh_token, format="json"
    )

    assert response.status_code == 401
