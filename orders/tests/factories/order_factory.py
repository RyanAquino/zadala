from orders.models import Order
from factory.django import DjangoModelFactory
from authentication.tests.factories.user_factory import UserFactory
import factory
import datetime


class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    customer = factory.SubFactory(UserFactory)
    date_ordered = factory.LazyFunction(datetime.datetime.now)
    complete = False
