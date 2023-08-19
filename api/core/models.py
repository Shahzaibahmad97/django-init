from rest_framework import status
from django.conf import settings
from django.db import models
from django.utils.timezone import now


class CreatedByModel(models.Model):
    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        abstract = True


class CreatedAtModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class UpdatedAtModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseModel(CreatedAtModel, UpdatedAtModel):
    class Meta:
        abstract = True


class CustomFieldMixin(models.Model):
    custom_fields = models.JSONField(default=dict)

    class Meta:
        abstract = True


class DecimalSize():
    def __init__(self, decimal_place, max_digits) -> None:
        self.DECIMAL_PLACES = decimal_place
        self.MAX_DIGITS = max_digits


class DecimalSizes():
    Price = DecimalSize(2, 12)
    Measurements = DecimalSize(2, 12)


class CharFieldSizes():
    SMALL = 50
    MEDIUM = 100
    LARGE = 150
    X_Large = 200
    XX_LARGE = 250
    XXX_LARGE = 500
    MAX = 5000


class MediaTypes():
    JSON = 'application/json'
    FORM = 'multipart/form-data'
    FORM_URL_ENCODED = 'application/x-www-form-urlencoded'


class CustomResponse:
    def __init__(self, code, message, http_code) -> None:
        self.code = code
        self.message = message
        self.http_code = http_code


class GlobalResponseMessages:
    un_authenticated = CustomResponse(4001, "Invalid Credentials!", status.HTTP_401_UNAUTHORIZED)
    missing_params = CustomResponse(4002, "Missing required information!", status.HTTP_400_BAD_REQUEST)
    serializer_error = CustomResponse(4004, "Serializer Error", status.HTTP_400_BAD_REQUEST)
    record_not_found = CustomResponse(4004, "Record not found!", status.HTTP_404_NOT_FOUND)
    something_went_wrong = CustomResponse(5001, "Something went wrong!", status.HTTP_503_SERVICE_UNAVAILABLE)

