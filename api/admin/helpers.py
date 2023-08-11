from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from api.core.email_helper import REPLACE_NOTIFICATION
from api.countries.models import Country


def send_review_notification(email, message_to_send, user_name, status):
    context = dict(
        message=message_to_send,
        title=f"Hi {user_name}, "
    )

    email_html_message = render_to_string('email/replace_notifications.html', context)  # noqa

    send_mail(
        f'Your job was {status}',
        f'Your job was {status}',
        settings.DEFAULT_FROM_EMAIL,
        [email],
        html_message=email_html_message,
        fail_silently=True
    )


def send_replace_notification(email, message_to_send, user_name, item_to_replace):
    context = dict(
        message=message_to_send,
        title=f"Hi {user_name}, ",
        item=item_to_replace.title,
        **REPLACE_NOTIFICATION
    )

    email_html_message = render_to_string('email/replace_notifications.html', context)  # noqa

    send_mail(
        f'Your {item_to_replace.__str__()} was replaced',
        f'Your {item_to_replace.__str__()} was replaced',
        settings.DEFAULT_FROM_EMAIL,
        [email],
        html_message=email_html_message,
        fail_silently=True
    )

