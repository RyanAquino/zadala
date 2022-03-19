from datetime import datetime

import factory
from factory import PostGenerationMethodCall
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyNaiveDateTime

from authentication.models import User
from authentication.validators import AuthProviders


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: "user%s@email.com" % n)
    first_name = "customer"
    last_name = "account"
    password = PostGenerationMethodCall("set_password", "password")
    is_active = True
    auth_provider = AuthProviders.email.value
    date_joined = FuzzyNaiveDateTime(datetime(2022, 1, 1))
    last_login = FuzzyNaiveDateTime(datetime(2022, 1, 1))

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for group in extracted:
                self.groups.add(group)
