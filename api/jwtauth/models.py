from rest_framework import status

from django.core.validators import MaxLengthValidator
from datetime import timedelta
from django.utils import timezone
from typing_extensions import OrderedDict
from django.db import models
from django.db.models.base import Model
from enum import Enum

from api.jwtauth import helpers
from api.core.models import CharFieldSizes, CustomResponse, GlobalResponseMessages


class OTPtypes(Enum):
    CREATE_USER = 'create'
    FORGOT_PASSWORD = 'forgot'

    @staticmethod
    def get_enum_set():
        return set(item.value for item in OTPtypes)

    @staticmethod
    def choices():
        return [(item.value, item.value) for item in OTPtypes]


class OTP(models.Model):
    code = models.CharField(max_length=CharFieldSizes.SMALL)
    email = models.EmailField()
    verification_token = models.CharField(max_length=CharFieldSizes.XXX_LARGE)
    timeout = models.DateTimeField()
    type = models.CharField(max_length=CharFieldSizes.SMALL)
    used = models.BooleanField(default=False)
  
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.verification_token = helpers.get_otp_verified_token(otp=self.code, email=self.email)

    def get_key(self):
        return '_'.join([str(self.type), self.email])

    def __str__(self) -> str:
        return self.email


class ResponseMessage(GlobalResponseMessages):
    user_already_exists = CustomResponse(4009, "User already exists!", status.HTTP_409_CONFLICT)
    invalid_otp_type = CustomResponse(4010, "Invalid otp type!", status.HTTP_400_BAD_REQUEST)
    otp_already_used = CustomResponse(4011, "OTP is already used!", status.HTTP_401_UNAUTHORIZED)
    otp_expired = CustomResponse(4012, "OTP expired!", status.HTTP_401_UNAUTHORIZED)
    wrong_otp_code = CustomResponse(4013, "OTP code is not correct!", status.HTTP_401_UNAUTHORIZED)
    verification_token_expired = CustomResponse(4005, "Token expired!", status.HTTP_401_UNAUTHORIZED)
  
