from django.contrib.auth.models import Group
from authentication.models import User


def base_data():
    GROUPS = ["Admins", "Customers", "Suppliers"]

    for group in GROUPS:
        Group.objects.get_or_create(name=group)

    User.objects.create_user(
        email="customer@email.com",
        password="password",
        first_name="customer",
        last_name="account",
        role="Customers",
    )
