import datetime

import factory
from factory.django import DjangoModelFactory

from authentication.tests.factories.user_factory import UserFactory
from orders.models import ShippingAddress
from orders.tests.factories.order_factory import OrderFactory


class ShippingAddressFactory(DjangoModelFactory):
    class Meta:
        model = ShippingAddress

    customer = factory.SubFactory(UserFactory)
    order = factory.SubFactory(OrderFactory)
    address = "address"
    city = "city"
    state = "state"
    zipcode = "1AA"
    date_added = factory.LazyFunction(datetime.datetime.now)
