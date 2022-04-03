from datetime import datetime

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    Group,
    PermissionsMixin,
)
from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.db import models
from django.dispatch import receiver
from rest_framework_simplejwt.tokens import RefreshToken

from authentication import aws_operations
from authentication.validators import AuthProviders, UserTokens


class UserManager(BaseUserManager):
    def create_user(self, **fields):
        email = self.normalize_email(fields["email"])
        user = self.model(email=email)
        user.first_name = fields["first_name"]
        user.last_name = fields["last_name"]
        user.set_password(fields["password"])
        customers_group = Group.objects.get(name=fields["role"])

        user.save(using=self._db)
        user.groups.add(customers_group)

        return user

    def create_superuser(self, email, first_name, last_name, password):

        data = {
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
            "role": "Admins",
        }
        admin = self.create_user(**data)
        admin.is_staff = True
        admin.is_superuser = True

        admin.save(using=self._db)

        return admin


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    last_login = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    auth_provider = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        default=AuthProviders.email.value,
        choices=AuthProviders.valid_providers(),
    )

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "password"]

    objects = UserManager()

    def tokens(self) -> UserTokens:
        refresh = RefreshToken.for_user(self)
        return UserTokens(
            **{"refresh": str(refresh), "token": str(refresh.access_token)}
        )

    def __str__(self):
        return self.email


@receiver(user_logged_in)
def on_login_success(sender, user, request, **kwargs):
    user_agent = request.headers.get("User-Agent")
    remote_address = request.META.get("REMOTE_ADDR")
    current_utc_timestamp = datetime.today().utcnow().strftime("%Y-%m-%d %H:%M:%S")

    message = {
        "user_id": user.id,
        "user_agent": user_agent,
        "remote_address": remote_address,
        "event": "login_success",
        "timestamp": user.last_login.strftime("%Y-%m-%d %H:%M:%S"),
    }

    sns_operations = aws_operations.SNSOperations()
    sns_operations.publish_message(
        subject=f"login_event_{current_utc_timestamp}", message=message
    )


@receiver(user_login_failed)
def on_login_failed(sender, request, **kwargs):
    user_agent = request.headers.get("User-Agent")
    remote_address = request.META.get("REMOTE_ADDR")
    current_utc_timestamp = datetime.today().utcnow().strftime("%Y-%m-%d %H:%M:%S")

    message = {
        "user_id": 0,
        "user_agent": user_agent,
        "remote_address": remote_address,
        "event": "login_failed",
        "timestamp": current_utc_timestamp,
    }
    sns_operations = aws_operations.SNSOperations()
    sns_operations.publish_message(
        subject=f"login_event_{current_utc_timestamp}", message=message
    )
