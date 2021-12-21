import datetime

import factory
from factory.django import DjangoModelFactory

from authentication.tests.factories.user_factory import UserFactory
from orders.models import Order


class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    customer = factory.SubFactory(UserFactory)
    date_ordered = factory.LazyFunction(datetime.datetime.now)
    complete = False
