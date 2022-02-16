from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from social_auth.google import Google


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        try:
            user_data = Google.validate(auth_token)
        except ValueError:
            raise serializers.ValidationError(
                "The token is invalid or expired. Please login again."
            )

        if user_data.get("aud") != settings.GOOGLE_CLIENT_ID:
            raise AuthenticationFailed("Please login using a valid Google token.")

        return user_data
