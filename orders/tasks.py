from typing import Dict

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from validate_email import validate_email


def send_email_notification(
    customer_email: str, template: str, subject: str, context_data: Dict
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
