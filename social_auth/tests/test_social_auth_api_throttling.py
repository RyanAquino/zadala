from unittest.mock import patch

import pytest
from django.core.cache import cache


@pytest.mark.django_db
class TestSocialAUthAPILoginThrottling:
    def teardown(self):
        cache.clear()

    @patch("rest_framework.throttling.SimpleRateThrottle.get_rate", lambda x: "10/day")
    def test_oauth_login_throttle_should_proceed_when_user_tokens_are_different(
        self, client
    ):
        """
        Test OAuth User login on 3 failed login attempts on different user tokens should not raise any throttling errors
        """
        max_attempts_threshold = 3
        data = None

        for i in range(max_attempts_threshold):
            data = {"auth_token": f"some-random-invalid-token-{i}"}
            client.post("/v1/social-auth/google/", data)

        response = client.post("/v1/social-auth/google/", data)
        assert response.status_code == 400 and response.json() == {
            "auth_token": ["The token is invalid or expired. Please login again."]
        }

    @patch("rest_framework.throttling.SimpleRateThrottle.get_rate", lambda x: "10/day")
    def test_oauth_login_throttle_should_raise_error_on_3_failed_attempts_with_same_token(
        self, client
    ):
        """
        Test OAuth User login on 3 failed login attempts of the same user token should fail
        given that 10 per day is the limit
        """
        max_attempts_threshold = 3
        data = {"auth_token": "sample-oauth-token"}

        for i in range(max_attempts_threshold):
            client.post("/v1/social-auth/google/", data)

        response = client.post("/v1/social-auth/google/", data)

        assert response.status_code == 429 and response.json()
