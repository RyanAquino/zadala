from unittest.mock import patch

from orders.tasks import send_email_notification


@patch("django.core.mail.send_mail", lambda **kwargs: kwargs)
@patch("validate_email.validate_email", lambda z, x: x)
def test_send_email_notification_task():
    """
    Test sending of email task
    """
    send_email_notification(
        "test_email@gmail.com",
        "invoice_email_template.html",
        "subject",
        {"context": None},
    )
