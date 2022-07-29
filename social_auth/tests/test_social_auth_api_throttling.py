from unittest.mock import patch

import pytest
from django.core.cache import cache


@pytest.mark.django_db
class TestSocialAuthAPILoginThrottling:
    def teardown(self):
        cache.clear()

    @patch("google.oauth2.id_token.verify_oauth2_token")
    @patch("rest_framework.throttling.SimpleRateThrottle.get_rate", lambda x: "10/day")
    def test_oauth_login_throttle_should_proceed_when_user_tokens_are_different(
        self, mocked_id_token, client
    ):
        """
        Test OAuth User login on 3 failed login attempts on different user tokens should not raise any throttling errors
        """
        max_attempts_threshold = 3
        data = {"auth_token": f"some-random-invalid-token"}
        mocked_id_token.side_effect = ValueError()

        for i in range(max_attempts_threshold):
            invalid_token = {"auth_token": f"some-random-invalid-token-{i}"}
            client.post("/v1/social-auth/google/", invalid_token)

        response = client.post("/v1/social-auth/google/", data)
        assert response.status_code == 400 and response.json() == {
            "auth_token": ["The token is invalid or expired. Please login again."]
        }

    @patch("google.oauth2.id_token.verify_oauth2_token")
    @patch("rest_framework.throttling.SimpleRateThrottle.get_rate", lambda x: "10/day")
    def test_oauth_login_throttle_should_raise_error_on_3_failed_attempts_with_same_token(
        self, mocked_id_token, client
    ):
        """
        Test OAuth User login on 3 failed login attempts of the same user token should fail
        given that 10 per day is the limit
        """
        max_attempts_threshold = 3
        data = {"auth_token": "sample-oauth-token"}
        mocked_id_token.side_effect = ValueError()

        for i in range(max_attempts_threshold):
            client.post("/v1/social-auth/google/", data)

        response = client.post("/v1/social-auth/google/", data)

        assert response.status_code == 429 and response.json()
