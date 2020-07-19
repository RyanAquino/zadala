from django.db import models
from django.contrib.auth.models import AbstractBaseUser, Group, BaseUserManager, Permission
from rest_framework_simplejwt.tokens import RefreshToken


class SupplierManager(BaseUserManager):

    def create_user(self, **fields):
        email = self.normalize_email(fields['email'])
        supplier = self.model(email=email)
        supplier.first_name = fields['first_name']
        supplier.last_name = fields['last_name']
        supplier.set_password(fields['password'])

        suppliers_group = Group.objects.get(name='Suppliers')

        supplier.save(using=self._db)
        supplier.groups.add(suppliers_group)

        return supplier


class SupplierPermissionsMixin(models.Model):
    """
    Add the fields and methods necessary to support the Group and Permission
    models using the ModelBackend.
    """
    groups = models.ManyToManyField(Group, blank=True)
    user_permissions = models.ManyToManyField(Permission, blank=True)

    class Meta:
        abstract = True


class Supplier(AbstractBaseUser, SupplierPermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    last_login = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password']

    objects = SupplierManager()

    def tokens(self, user):
        print(user)
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'token': str(refresh.access_token)
        }

    def __str__(self):
        return self.email
