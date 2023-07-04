import time
from unittest.mock import patch

import pytest
from django.core.cache import cache

from authentication.tests.factories.user_factory import UserFactory


@pytest.mark.django_db
class TestAPILoginThrottling:
    def teardown_method(self):
        cache.clear()

    @patch("rest_framework.throttling.SimpleRateThrottle.get_rate", lambda x: "10/day")
    @patch("botocore.client.BaseClient._make_api_call", lambda *args, **kwargs: None)
    def test_login_throttle_should_raise_error_on_3_failed_attempts_with_same_user(
        self, client
    ):
        """
        Test User login on 3 failed login attempts of the same user should fail given that 10 per day is the limit
        """
        user = UserFactory()
        max_attempts_threshold = 3
        data = {"email": user.email, "password": "wrong-password"}

        for i in range(max_attempts_threshold):
            client.post("/v1/auth/login/", data)

        response = client.post("/v1/auth/login/", data)

        assert response.status_code == 429 and response.json()

    # Test for overridden method in custom_throttle.py allow_request()
    @patch("rest_framework.throttling.SimpleRateThrottle.get_rate", lambda x: None)
    @patch("botocore.client.BaseClient._make_api_call", lambda *args, **kwargs: None)
    def test_login_throttle_should_not_raise_error_given_rate_is_none(self, client):
        """
        Test User login when rate is not set
        """
        user = UserFactory()
        data = {"email": user.email, "password": "password"}
        response = client.post("/v1/auth/login/", data)

        assert response.status_code == 200

    # Test for overridden method in custom_throttle.py allow_request()
    @patch(
        "rest_framework.throttling.AnonRateThrottle.get_cache_key", lambda x, y, z: None
    )
    @patch("botocore.client.BaseClient._make_api_call", lambda *args, **kwargs: None)
    def test_login_throttle_should_not_raise_error_given_cache_key_is_none(
        self, client
    ):
        """
        Test User login when cache key got no results
        """
        user = UserFactory()
        data = {"email": user.email, "password": "password"}
        response = client.post("/v1/auth/login/", data)

        assert response.status_code == 200

    @patch("rest_framework.throttling.SimpleRateThrottle.get_rate", lambda x: "10/day")
    @patch("rest_framework.throttling.SimpleRateThrottle.timer")
    @patch("botocore.client.BaseClient._make_api_call", lambda *args, **kwargs: None)
    def test_login_throttle_should_remove_cache_keys_with_past_datetime(
        self, mocked_timer, client
    ):
        """
        Test User login throttle should remove cache keys that were saved in past datetime
        """
        user = UserFactory()
        some_future_time_in_seconds = 99999999999
        data = {"email": user.email, "password": "wrong-password"}

        mocked_timer.return_value = time.time()
        client.post("/v1/auth/login/", data)

        mocked_timer.return_value = some_future_time_in_seconds
        response = client.post("/v1/auth/login/", data)

        assert response.status_code == 403 and response.json()

    @patch("rest_framework.throttling.SimpleRateThrottle.get_rate", lambda x: "10/day")
    @patch("botocore.client.BaseClient._make_api_call", lambda *args, **kwargs: None)
    def test_login_throttle_should_proceed_when_users_are_different(self, client):
        """
        Test User login on 3 failed login attempts on different users should not raise any throttling errors
        """
        UserFactory.create_batch(3)
        max_attempts_threshold = 3
        data = None

        for i in range(max_attempts_threshold):
            data = {"email": f"user{i}@email.com", "password": "wrong-password"}
            client.post("/v1/auth/login/", data)

        response = client.post("/v1/auth/login/", data)
        assert response.status_code == 403 and response.json()
