from collections import Counter
from copy import copy

from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.throttling import AnonRateThrottle

from social_auth.serializers import GoogleSocialAuthSerializer


class UserLoginRateThrottle(AnonRateThrottle):
    scope = "logins"
    max_attempts = 3

    def allow_request(self, request: Request, view):
        """
        Implement the check to see if the request should be throttled.

        On success calls `throttle_success`.
        On failure calls `throttle_failure`.
        """
        if self.rate is None:
            return True

        self.key = self.get_cache_key(request, view)
        if self.key is None:
            return True

        self.history = self.cache.get(self.key, [])
        self.now = self.timer()
        failed = False

        if self.history:
            last_login_attempt = self.history[-1]

            if isinstance(self.history[-1], str):
                last_login_attempt = float(self.history[-1].split("_")[-1])

            while self.history and last_login_attempt <= self.now - self.duration:
                self.history.pop()

        if len(self.history) >= self.num_requests:
            return self.throttle_failure()

        if len(self.history) >= self.max_attempts:
            failed = self.verify_fail_login_attempts(request)

        return (
            self.throttle_failure()
            if failed is True
            else self.throttle_success(request)
        )

    def format_history_exclude_timestamp(self):
        """
        Helper method to format history and exclude its timestamps
        """
        history_copy = copy(self.history)

        for index, history in enumerate(history_copy):
            if isinstance(history, str):
                history_excluded_timestamp = history.split("_")[:-1]
                history_copy[index] = "_".join(history_excluded_timestamp)

        return history_copy

    def verify_fail_login_attempts(self, request: Request) -> bool:
        """
        Verify fail login attempts
        """
        email = request.data.get("email")
        password = request.data.get("password")

        formatted_history = self.format_history_exclude_timestamp()
        history_count_mapping: dict = Counter(formatted_history)

        for key, value in history_count_mapping.items():
            cached_email = key.split("_")[-2]
            cached_password = key.split("_")[-1]

            if (
                cached_email == email
                and cached_password == password
                and value >= self.max_attempts
            ):
                self.max_attempts = 0
                return True
        return False

    def throttle_success(self, request) -> bool:
        """
        Inserts the current request's timestamp along with the key
        into the cache.
        """
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)

        if not user:
            self.history.insert(0, f"failed_login_{email}_{password}_{self.now}")
        self.cache.set(self.key, self.history, self.duration)

        return True

    def wait(self) -> float:
        """
        Returns the recommended next request time in seconds.
        """
        remaining_duration = self.duration

        if self.history:
            last_history_copy = self.history[-1]
            if isinstance(last_history_copy, str):
                last_history_copy = float(last_history_copy.split("_")[-1])
            remaining_duration = self.duration - (self.now - last_history_copy)

        available_requests = (
            1 if not self.max_attempts else self.num_requests - len(self.history) + 1
        )

        return remaining_duration / float(available_requests)


class OAuthUserLoginRateThrottle(UserLoginRateThrottle):
    def verify_fail_login_attempts(self, request: Request) -> bool:
        auth_token = request.data.get("auth_token")
        formatted_history = self.format_history_exclude_timestamp()
        history_count_mapping: dict = Counter(formatted_history)

        for key, value in history_count_mapping.items():
            cached_oauth_token = key.split("_")[-1]

            if cached_oauth_token == auth_token and value >= self.max_attempts:
                self.max_attempts = 0
                return True
        return False

    def throttle_success(self, request) -> bool:
        serializer = GoogleSocialAuthSerializer(data=request.data)
        auth_token = request.data.get("auth_token")

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            self.history.insert(0, f"failed_login_oauth_{auth_token}_{self.now}")
        self.cache.set(self.key, self.history, self.duration)

        return True
