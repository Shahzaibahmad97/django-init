import base64
from io import BytesIO
import qrcode

from django.db.models import Subquery
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.exceptions import APIException, _get_error_details
from rest_framework.views import exception_handler

from api.core.models import CustomResponse


class DotsValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Invalid input.')
    default_code = 'non_field'
    key = 'validations'

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        # For validation failures, we may collect many errors together,
        # so the details should always be coerced to a list if not already.
        if not isinstance(detail, dict) and not isinstance(detail, list):
            detail = {'non_field': [detail]}

        self.detail = _get_error_details(detail, code)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None and type(exc):
        if response.data.get('detail'):
            custom_response = dict(
                key='validations',
                messages={
                    "non_field": [response.data['detail']]
                })
        elif response.data.get('non_field_errors'):
            custom_response = dict(
                key='validations',
                messages={
                    "non_field": [response.data['non_field_errors']]
                })
        else:
            custom_response = dict(key='validations', messages=response.data)
        response.data = custom_response
        return response

    return response


class ArraySubquery(Subquery):  # noqa
    template = 'ARRAY(%(subquery)s)'


def generate_qr_code(data, return_base64=True):
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,  # QR code version (1 to 40)
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
        box_size=10,  # Size of each box in pixels
        border=4,     # Border size in boxes
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR code instance
    img = qr.make_image(fill_color="black", back_color="white")
    if return_base64:
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        qr = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return qr
