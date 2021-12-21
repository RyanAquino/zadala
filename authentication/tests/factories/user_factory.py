import factory
from factory import PostGenerationMethodCall
from factory.django import DjangoModelFactory

from authentication.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: "user%s@email.com" % n)
    first_name = "customer"
    last_name = "account"
    password = PostGenerationMethodCall("set_password", "password")
    is_active = True

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for group in extracted:
                self.groups.add(group)
