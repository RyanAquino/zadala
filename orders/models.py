from typing import Dict

from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags
from pydantic import EmailStr
from validate_email import validate_email

from authentication.models import User
from products.models import Product


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        order_items = self.orderitem_set.all()

        for i in order_items:
            if not i.product.digital:
                shipping = True

        return shipping

    @property
    def order_items(self):
        return self.orderitem_set.all()

    @property
    def get_cart_total(self):
        items = self.order_items
        total = sum([item.total for item in items])
        return total

    @property
    def get_cart_items(self):
        items = self.order_items
        total = sum([item.quantity for item in items])
        return total

    @staticmethod
    def send_email_notification(
        customer_email: EmailStr, template: str, subject: str, context_data: Dict
    ):
        if validate_email(email_address=customer_email, check_smtp=False):
            html_message = render_to_string(template, context_data)
            plain_message = strip_tags(html_message)

            send_mail(
                subject,
                plain_message,
                settings.EMAIL_HOST_USER,
                [customer_email, settings.EMAIL_HOST_USER],
                fail_silently=False,
                html_message=html_message,
            )


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True)
    date_added = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return str(self.id)

    @property
    def total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # pragma: no cover
        return str(self.address)


@receiver(post_delete, sender="orders.OrderItem")
def delete_order(sender, instance: OrderItem, **kwargs):
    order_id = instance.order_id
    order_items = OrderItem.objects.filter(order_id=instance.order_id).count()

    if order_items == 0:
        Order.objects.get(pk=order_id).delete()
