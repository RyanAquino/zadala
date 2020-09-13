from django.contrib.auth.models import Group
import factory


class CustomersGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    name = "Customers"


class SuppliersGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    name = "Suppliers"


class AdminsGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    name = "Admins"
