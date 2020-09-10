import pytest
from rest_framework.test import APITestCase
from base_data import base_data


class TestAuthenticationAPI(APITestCase):
    allow_database_queries = True

    @pytest.mark.django_db
    def test_user_register(self):
        """
        Test User registration
        """
        base_data()
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
        base_data()
        data = {"email": "customer@email.com", "password": "password"}

        response = self.client.post("/api/auth/login", data, format="json")
        data = response.json()

        assert data['email'] == 'customer@email.com'
        assert data['first_name'] == 'customer'
        assert data['last_name'] == 'account'
        assert data['access'] and data['refresh']
        assert response.status_code == 200
