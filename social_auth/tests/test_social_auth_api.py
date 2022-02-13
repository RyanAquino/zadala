from unittest.mock import patch

import pytest

from authentication.tests.factories.user_factory import UserFactory
from social_auth.google import Google


@pytest.mark.django_db
@patch("google.oauth2.id_token.verify_oauth2_token")
@patch("django.conf.settings.GOOGLE_CLIENT_ID", 1)
def test_social_login_non_existing_account(mocked_oauth_details, client):
    """
    Test Social User login should create and return tokens for account
    """
    data = {"auth_token": "some-oauth-token"}
    mocked_oauth_details.return_value = {
        "iss": "accounts.google.com",
        "aud": 1,
        "email": "test-user@gmail.com",
        "given_name": "given-name-test-user",
        "family_name": "family-name-test-user",
    }

    response = client.post("/v1/social-auth/google/", data, format="json")
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["email"] == "test-user@gmail.com"
    assert response_data.get("access") and response_data.get("refresh")


@pytest.mark.django_db
@patch("google.oauth2.id_token.verify_oauth2_token")
@patch("django.conf.settings.GOOGLE_CLIENT_ID", 1)
def test_social_login_on_existing_account(mocked_oauth_details, client):
    """
    test Social user login on an existing account should return tokens
    """
    user = UserFactory(email="test@gmail.com", password="temp-password")
    data = {"auth_token": "some-oauth-token"}
    mocked_oauth_details.return_value = {
        "iss": "accounts.google.com",
        "aud": 1,
        "email": user.email,
    }

    response = client.post("/v1/social-auth/google/", data, format="json")
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["email"] == "test@gmail.com"
    assert response_data.get("access") and response_data.get("refresh")


@patch("social_auth.google.Google.validate")
def test_social_login_invalid_token(mocked_google_validate, client):
    """
    Test social login with invalid/expired token
    """
    mocked_google_validate.side_effect = ValueError("mocked error")
    data = {"auth_token": "test-oauth-invalid-token"}

    response = client.post("/v1/social-auth/google/", data, format="json")
    response_data = response.json()

    assert response.status_code == 400
    assert response_data == {
        "auth_token": ["The token is invalid or expired. Please login again."]
    }


@patch("django.conf.settings.GOOGLE_CLIENT_ID", "some-random-number")
@patch("google.oauth2.id_token.verify_oauth2_token")
def test_social_login_invalid_token_audience_mismatch(mocked_oauth_details, client):
    """
    Test social login with invalid Google token
    """
    data = {"auth_token": "test-oauth-invalid-token"}
    mocked_oauth_details.return_value = {
        "iss": "accounts.google.com",
        "aud": "another-random-number",
        "email": "test-user@gmail.com",
        "given_name": "given-name-test-user",
        "family_name": "family-name-test-user",
    }

    response = client.post("/v1/social-auth/google/", data, format="json")
    response_data = response.json()

    assert response.status_code == 403
    assert response_data == {"detail": "Please login using a valid Google token."}


def test_google_validate_on_invalid_token():
    """
    Test Google token validator should raise ValueError on invalid token
    """
    with pytest.raises(ValueError):
        Google.validate("some-invalid-token")
