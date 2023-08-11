from random import randint
import base64

from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from api.core.constants import DeviceType
from api.core.email_helper import ACTIVATE_EMAIL_MOBILE, ACTIVATE_EMAIL_WEB
from api.users.helper import generate_code


def send_confirmation_email(request, new_otp):
    context = dict(code=f"{new_otp.code}",
                    name=new_otp.email.split('@')[0], **ACTIVATE_EMAIL_MOBILE)
    email_html_message = render_to_string('email/activate-email.html', context)

    send_mail(
        'Homme email confirmation',
        '',
        settings.DEFAULT_FROM_EMAIL,
        [new_otp.email],
        html_message=email_html_message,
        fail_silently=False,
    )


def get_random_otp():
    return str(randint(1000, 9999))


def get_otp_verified_token(otp, email):
    token_str = get_random_otp() + email + otp
    token_str_bytes = token_str.encode('ascii')
    base64_bytes = base64.b64encode(token_str_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message


