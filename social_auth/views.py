from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from authentication.custom_throttle import OAuthUserLoginRateThrottle
from authentication.models import User
from authentication.serializers import UserSerializer
from authentication.validators import AuthProviders, UserLogin
from social_auth.serializers import GoogleSocialAuthSerializer


class GoogleSocialAuthView(GenericAPIView):
    authentication_classes: list = []
    permission_classes: list = []
    serializer_class = GoogleSocialAuthSerializer
    throttle_classes = [OAuthUserLoginRateThrottle]

    def post(self, request):
        """
        POST with "auth_token"
        Send an idtoken as from google to get user information
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_user_data = serializer.validated_data.get("auth_token")
        oauth_user_password = settings.GOOGLE_CLIENT_SECRET
        user_data = {
            "email": validated_user_data.get("email"),
            "first_name": validated_user_data.get("given_name"),
            "last_name": validated_user_data.get("family_name"),
            "password": oauth_user_password,
        }

        try:
            user = User.objects.get(email=user_data.get("email"))

            if user.auth_provider == AuthProviders.email.value:
                raise AuthenticationFailed(
                    {"email": "Please login using your provider"}
                )
        except User.DoesNotExist:
            user_serializer = UserSerializer(data=user_data)
            user = user_serializer.create(user_data)
            user.auth_provider = AuthProviders.google.value
            user.save()

        user = authenticate(email=user.email, password=oauth_user_password)
        update_last_login(sender=None, user=user)
        tokens = user.tokens()
        user_details = UserLogin(
            **{
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "access": tokens.token,
                "refresh": tokens.refresh,
            }
        )

        return Response(user_details.dict(), status=status.HTTP_200_OK)
