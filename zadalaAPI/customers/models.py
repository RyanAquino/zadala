from django.db import models
from django.contrib.auth.models import AbstractBaseUser, Group, BaseUserManager, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken


class CustomerManager(BaseUserManager):

    def create_user(self, **fields):
        email = self.normalize_email(fields['email'])
        customer = self.model(email=email)
        customer.first_name = fields['first_name']
        customer.last_name = fields['last_name']
        customer.set_password(fields['password'])
        customers_group = Group.objects.get(name='Customers')

        customer.save(using=self._db)
        customer.groups.add(customers_group)

        return customer

    def create_superuser(self, email, first_name, last_name, password):

        data = {
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'password': password
        }
        admin = self.create_user(**data)
        admins_group = Group.objects.get(name='Admins')
        admin.is_staff = True
        admin.is_superuser = True

        admin.save(using=self._db)
        admin.groups.add(admins_group)

        return admin


class Customer(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    last_login = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password']

    objects = CustomerManager()

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'token': str(refresh.access_token)
        }

    def __str__(self):
        return self.email
