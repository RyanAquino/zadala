import factory
from factory.django import DjangoModelFactory

from categories.models import Category


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"Category {n}")
