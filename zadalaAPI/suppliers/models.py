from django.db import models
from django.contrib.auth.models import AbstractBaseUser, Group, BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken


class SupplierManager(BaseUserManager):

    def create_user(self, **fields):
        email = self.normalize_email(fields['email'])
        supplier = self.model(email=email)
        supplier.first_name = fields['first_name']
        supplier.last_name = fields['last_name']
        supplier.set_password(fields['password'])
        supplier.save(using=self._db)

        return fields


class Supplier(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING, default=3)
    password = models.CharField(max_length=255)
    last_login = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password']

    objects = SupplierManager()

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'token': str(refresh.access_token)
        }

    def __str__(self):
        return self.email
