import re
from hmac import compare_digest

from django.utils import timezone
from django.utils.translation import gettext as _
from django_rest_passwordreset.serializers import PasswordTokenSerializer
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from api.core import helper

from api.core.constants import DeviceType
from api.core.utils import DotsValidationError
from api.core.validator import PasswordValidator
from api.jwtauth.helpers import send_confirmation_email
from api.jwtauth.models import OTPtypes
from api.users.helper import generate_code
from api.users.models import SalonProfile, User, UserProfile


class OTPSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    otp_type = serializers.ChoiceField(OTPtypes.choices(), write_only=True)


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    otp_type = serializers.ChoiceField(OTPtypes.choices(), write_only=True)
    otp_code = serializers.CharField(write_only=True)


class UserCreateSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(
        write_only=True, required=True, validators=[
            PasswordValidator.one_symbol,
            PasswordValidator.lower_letter,
            PasswordValidator.upper_letter,
            PasswordValidator.number
        ]
    )

    class Meta:
        model = User
        fields = (
            "phone", "role", "email", "password", "confirm_password",
        )

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise DotsValidationError({"email": "User with this Email address already exists."})
        return value

    @classmethod
    def _validate_password(cls, validated_data):
        password = validated_data.pop("password")
        confirm_password = validated_data.pop("confirm_password")
        if not compare_digest(password, confirm_password):
            raise serializers.ValidationError({"password": _("Password does not match")})
        return password

    def create(self, validated_data):
        password = self._validate_password(validated_data)

        self.pre_create(validated_data)
        user = super(UserCreateSerializer, self).create(validated_data)

        user.set_password(password)
        user.updated_at = timezone.now()
        user.save()
        return user

    def pre_create(self, validated_data):
        ...


class UserProfileCreateSerializer(serializers.ModelSerializer):
    role = serializers.HiddenField(default=User.Role.USER)
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(required=True)
    verification_token = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(
        write_only=True, required=True, validators=[
            PasswordValidator.one_symbol,
            PasswordValidator.lower_letter,
            PasswordValidator.upper_letter,
            PasswordValidator.number
        ]
    )

    class Meta:
        model = UserProfile
        fields = (
            "first_name", "last_name", "referrer", "salon", "stylist", 
            "phone", "role", "email", "password", "confirm_password", "verification_token",
        )
    
    def create(self, validated_data):
        user_data = {
            'email': validated_data.pop('email'),
            'profile_picture': validated_data.get('profile_picture', ''),
            'phone': validated_data.pop('phone'),
            'password': validated_data.pop('password'),
            'confirm_password': validated_data.pop('confirm_password'),
            'role': validated_data.pop('role')
        }
        user_serializer = UserCreateSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)

        validated_data['user'] = user_serializer.save()
        user_profile = super().create(validated_data)
        return user_profile


class SalonProfileCreateSerializer(serializers.ModelSerializer):
    role = serializers.HiddenField(default=User.Role.SALON)
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(required=True)
    verification_token = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(
        write_only=True, required=True, validators=[
            PasswordValidator.one_symbol,
            PasswordValidator.lower_letter,
            PasswordValidator.upper_letter,
            PasswordValidator.number
        ]
    )

    class Meta:
        model = SalonProfile
        fields = (
            "salon_name", "contact_name", 
            "phone", "role", "email", "password", "confirm_password", "verification_token",
        )
    
    def create(self, validated_data):
        user_data = {
            'email': validated_data.pop('email'),
            'profile_picture': validated_data.get('profile_picture', ''),
            'phone': validated_data.pop('phone'),
            'password': validated_data.pop('password'),
            'confirm_password': validated_data.pop('confirm_password'),
            'role': validated_data.pop('role')
        }
        user_serializer = UserCreateSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)

        validated_data['user'] = user_serializer.save()
        salon_profile = super().create(validated_data)
        return salon_profile


class ReturnJWTTokensSerializer(serializers.Serializer):  # noqa
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()


class LoginSerializer(TokenObtainPairSerializer):  # noqa
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user_id'] = user.id
        token['role'] = User.Role.ADMIN if user.is_superuser else user.role
        return token

    def validate(self, attrs):
        try:
            validate_attrs = super(LoginSerializer, self).validate(attrs)
        except Exception as e:
            raise DotsValidationError({"password": [str(e)]})

        self.user.last_login = timezone.now()
        self.user.updated_at = timezone.now()
        self.user.save(update_fields=['last_login', 'updated_at'])

        return validate_attrs


class CustomPasswordTokenSerializer(PasswordTokenSerializer):  # noqa
    password = serializers.CharField(label=_("Password"), style={'input_type': 'password'},
                                     validators=[
                                         PasswordValidator.one_symbol,
                                         PasswordValidator.lower_letter,
                                         PasswordValidator.upper_letter,
                                         PasswordValidator.number
                                     ])
