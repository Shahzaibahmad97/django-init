from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django_rest_passwordreset.views import ResetPasswordValidateToken, ResetPasswordConfirm, ResetPasswordRequestToken, \
    User
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenViewBase

from api.core.serializer import SuccessResponseSerializer
from api.core.utils import DotsValidationError
from api.jwtauth.models import OTP, OTPtypes, ResponseMessage

from .helpers import get_random_otp, send_confirmation_email
from .serializers import ReturnJWTTokensSerializer, LoginSerializer, SalonProfileCreateSerializer, UserCreateSerializer, \
    CustomPasswordTokenSerializer, UserProfileCreateSerializer, OTPSerializer, VerifyOTPSerializer
from ..core.constants import DeviceType
from ..core.mixin import GenericDotsViewSet
from api.core import helper

login_response = openapi.Response('Respond with jwt access&refresh token', ReturnJWTTokensSerializer)
refresh_response = openapi.Response('Respond with jwt access&refresh token, '
                                    'refresh is returned in case if', ReturnJWTTokensSerializer)


def verify_otp(token, email, otp_type):
    """ returns user otp and error response if found any """
    try:
        user_otp = OTP.objects.get(verification_token=token, email=email, type=otp_type)
        if timezone.now() > user_otp.timeout:
            raise DotsValidationError(ResponseMessage.verification_token_expired.message)
    except OTP.DoesNotExist:
        raise DotsValidationError(ResponseMessage.un_authenticated.message)

    # success case
    return user_otp


class OTPViewSet(GenericDotsViewSet):
    serializer_class = OTPSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['POST'], url_path='send', queryset=OTP.objects.all(),
            serializer_create_class=OTPSerializer)
    def generate_otp(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        otp_type = serializer.validated_data['otp_type']
        
        user = User.objects.filter(email=email)

        # check if otp is for create user then 
        if otp_type == OTPtypes.CREATE_USER.value:
            # if user already exists then it returns error
            if user.exists():
                raise DotsValidationError({'email': ResponseMessage.user_already_exists.message})
        else:
            if not user.exists():
                raise DotsValidationError({'email': ResponseMessage.record_not_found})
          
        # successfully create the otp for every type
        timeout = timezone.now() + timedelta(seconds=settings.OTP_TIMEOUT_SECONDS)
        new_otp = OTP.objects.create(code=get_random_otp(), email=email, type=otp_type, timeout=timeout)
        send_confirmation_email(request, new_otp)
        return helper.SuccessResponse("OTP sent successfully")

    @action(detail=False, methods=['PATCH'], url_path='verify', queryset=OTP.objects.all(),
        serializer_class=VerifyOTPSerializer)
    def verify_otp(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        otp_code = serializer.validated_data['otp_code']
        otp_type = serializer.validated_data['otp_type']

        user_otp = OTP.objects.filter(email=email, type=otp_type).order_by('-pk').first()
        if not user_otp:
            raise DotsValidationError({'email': ResponseMessage.record_not_found.message})   

        if user_otp.code != otp_code:
            raise DotsValidationError({'otp_code': ResponseMessage.wrong_otp_code})

        if user_otp.used:
            raise DotsValidationError({'otp_code': ResponseMessage.otp_already_used})   

        if timezone.now() > user_otp.timeout:
            raise DotsValidationError({'otp_code': ResponseMessage.otp_expired})

        # update the expiry time for verification code
        user_otp.used = True
        user_otp.timeout = timezone.now() + timedelta(seconds=settings.OTP_VERIFICATION_TIMEOUT_SECONDS)
        
        user_otp.save()
        return helper.SuccessResponse({ 'verification_token' :  user_otp.verification_token })


class RegistrationViewSet(GenericDotsViewSet):
    serializer_class = ReturnJWTTokensSerializer
    serializer_create_class = UserProfileCreateSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_create(data=request.data)
        serializer.is_valid(raise_exception=True)

        verification_token = serializer.validated_data.pop('verification_token')
        email = serializer.validated_data.get('email')

        verify_otp(token=verification_token, email=email, otp_type=OTPtypes.CREATE_USER.value)

        user_profile = serializer.save()
        # from api.users.models import UserProfile
        # user_profile = UserProfile.objects.get(id=3)
        # send_confirmation_email(request, user_profile)
        refresh = RefreshToken.for_user(user_profile)
        refresh['role'] = User.Role.ADMIN if user_profile.user.is_superuser else user_profile.user.role

        return Response(dict(refresh=str(refresh), access=str(refresh.access_token)))

    @action(detail=False, methods=['POST'], url_path='salon',
            serializer_create_class=SalonProfileCreateSerializer,)
    def create_salon(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_serializer_create(self, *args, **kwargs):
        serializer = self.get_serializer_create_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer(*args, **kwargs)


class LoginViewSet(TokenViewBase):
    serializer_class = LoginSerializer

    @swagger_auto_schema(request_body=LoginSerializer, responses={200: login_response})
    def post(self, request, *args, **kwargs):
        return super(LoginViewSet, self).post(request, *args, **kwargs)


class TokenRefreshView(TokenViewBase):
    serializer_class = TokenRefreshSerializer

    @swagger_auto_schema(request_body=TokenRefreshSerializer, responses={200: refresh_response})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomResetPasswordValidateToken(ResetPasswordValidateToken):
    permission_classes = [AllowAny]


class CustomResetPasswordConfirm(ResetPasswordConfirm):
    permission_classes = [AllowAny]
    serializer_class = CustomPasswordTokenSerializer


class CustomResetPasswordRequestToken(ResetPasswordRequestToken):
    permission_classes = [AllowAny]

