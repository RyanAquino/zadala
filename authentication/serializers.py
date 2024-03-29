from django.contrib.auth import user_logged_in
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from authentication.models import User
from authentication.validators import AuthProviders, UserLogin


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=65, min_length=8)
    email = serializers.EmailField(max_length=255, min_length=4)
    first_name = serializers.CharField(max_length=255, min_length=2)
    last_name = serializers.CharField(max_length=255, min_length=2)

    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = (
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
            "auth_provider",
        )

    def validate(self, attrs):
        email = attrs.get("email", "")

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "Email already in use"})
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data["role"] = "Customers"
        return User.objects.create_user(**validated_data)


class SupplierSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=65, min_length=8)
    email = serializers.EmailField(max_length=255, min_length=4)
    first_name = serializers.CharField(max_length=255, min_length=2)
    last_name = serializers.CharField(max_length=255, min_length=2)

    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = (
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
            "auth_provider",
        )

    def validate(self, attrs):
        email = attrs.get("email", "")

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "Email already in use"})
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data["role"] = "Suppliers"
        return User.objects.create_user(**validated_data)


class UserLoginSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=65, write_only=True)
    access = serializers.CharField(max_length=255, read_only=True)
    refresh = serializers.CharField(max_length=255, read_only=True)
    first_name = serializers.CharField(max_length=255, read_only=True)
    last_name = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "access", "refresh", "first_name", "last_name"]

    def validate(self, attrs) -> UserLogin:
        email = attrs.get("email", "")
        password = attrs.get("password", "")
        request = self.context.get("request")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise AuthenticationFailed("Invalid email/password")
        else:
            if not user.check_password(password):
                raise AuthenticationFailed("Invalid email/password")

        if user.auth_provider != AuthProviders.email.value:
            raise AuthenticationFailed("Please login using your login provider.")

        tokens = user.tokens()
        update_last_login(sender=None, user=user)
        user_logged_in.send(sender=user.__class__, request=request, user=user)

        return UserLogin(
            **{
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "access": tokens.token,
                "refresh": tokens.refresh,
            }
        )


class UserProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=65, min_length=8)
    email = serializers.EmailField(max_length=255, min_length=4)
    first_name = serializers.CharField(max_length=255, min_length=2)
    last_name = serializers.CharField(max_length=255, min_length=2)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "last_login",
            "auth_provider",
            "date_joined",
            "password",
        ]
        write_only_fields = ["password", "groups"]
        read_only_fields = ["auth_provider"]

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop("fields", None)

        super(UserProfileSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
