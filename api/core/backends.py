from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Prefetch, FileField
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from rest_framework_simplejwt.settings import api_settings

from api.core.constants import DeviceType
from api.users.models import User


class CustomJWTAuthentication(JWTAuthentication):
    def get_user_with_relations(self, user_id, request):
        return User.objects.filter(id=user_id).first()

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        return self.get_user(validated_token, request), validated_token

    def get_user(self, validated_token, request):
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise InvalidToken('Token contained no recognizable user identification')

        try:
            if request.path == '/api/me':
                user = self.get_user_with_relations(user_id, request)
            else:
                user = User.objects.get(**{api_settings.USER_ID_FIELD: user_id})

        except ObjectDoesNotExist:
            raise AuthenticationFailed('User not found', code='user_not_found')

        if not getattr(user, "is_active", False):
            raise AuthenticationFailed('User is inactive', code='user_inactive')

        if getattr(user, "is_blocked", False):
            raise AuthenticationFailed('Your account is blocked you are not able to authorize', code='user_blocked')

        return user


class CustomFileStorageFile(FileField):
    def generate_filename(self, instance, filename):
        # if instance.
        return super(CustomFileStorageFile, self).generate_filename(instance, filename)
