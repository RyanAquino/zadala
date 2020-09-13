import pytest
from rest_framework.test import APITestCase
from .base_data import base_data


class TestAuthenticationAPI(APITestCase):
    allow_database_queries = True

    def setUp(self) -> None:
        base_data()
        return super().setUp()

    @pytest.mark.django_db
    def test_user_register(self):
        """
        Test User registration
        """
        data = {
            "password": "password",
            "email": "customer@example.com",
            "first_name": "customer",
            "last_name": "account",
        }

        response = self.client.post("/api/auth/customer/register", data, format="json")

        assert response.status_code == 201

    def test_user_login(self):
        """
        Test User login
        """
        data = {"email": "customer@email.com", "password": "password"}

        response = self.client.post("/api/auth/login", data, format="json")
        data = response.json()

        assert data["email"] == "customer@email.com"
        assert data["first_name"] == "customer"
        assert data["last_name"] == "account"
        assert response.status_code == 200

    def test_tokens(self):
        """
        Test refresh token
        """
        data = {"email": "customer@email.com", "password": "password"}

        response = self.client.post("/api/auth/login", data, format="json")
        data = response.json()

        assert data["refresh"] and data["access"]

        refresh_token = {"refresh": data["refresh"]}
        response = self.client.post(
            "/api/auth/token/refresh", refresh_token, format="json"
        )

        assert response.status_code == 200
        assert response.json()["access"]

    def test_refresh_token_with_access_token(self):
        """
        Test refresh token with access token should fail
        """
        data = {"email": "customer@email.com", "password": "password"}

        response = self.client.post("/api/auth/login", data, format="json")
        data = response.json()
        refresh_token = {"refresh": data["access"]}
        response = self.client.post(
            "/api/auth/token/refresh", refresh_token, format="json"
        )

        assert response.status_code == 401
