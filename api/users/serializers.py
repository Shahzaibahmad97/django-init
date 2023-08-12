from hmac import compare_digest
from rest_framework import serializers
from django.contrib.auth import get_user_model
from api.core.utils import DotsValidationError

from api.core.validator import PasswordValidator
from api.core.constants import Status
from api.core import helper
from api.users.models import Stylist, UserProfile, SalonProfile, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'


class UserUpdateSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True,
                                         validators=[
                                             PasswordValidator.one_symbol,
                                             PasswordValidator.lower_letter,
                                             PasswordValidator.upper_letter,
                                             PasswordValidator.number
                                         ])
    confirm_password = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField()

    class Meta:
        model = get_user_model()
        fields =  ('id', 'email', 'current_password', 'new_password', 'confirm_password', 
                   'profile_picture', 'phone', 'fcm_token', 'role', )
        extra_kwargs = {'password': {'write_only': True}, 'fcm_token': {'write_only': True}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)
    
    def update(self, instance, validated_data):
        if (validated_data.get('email') and
                validated_data['email'] != instance.email and
                User.objects.filter(email=validated_data['email']).exists()):
            raise DotsValidationError('user with this email already exists.')

        if validated_data.get('email') == instance.email:
            del validated_data['email']

        password = validated_data.pop('current_password', None)
        new_password = validated_data.pop('new_password', None)
        confirm_password = validated_data.pop('confirm_password', None)

        if not instance.check_password(password):
            raise DotsValidationError({"current_password": ["Invalid password"]})

        if new_password:
            if compare_digest(password, new_password):
                raise DotsValidationError(
                    {"new_password": ["You new password should be different from the current one"]})

            if confirm_password != new_password:
                raise DotsValidationError({"confirm_password": ["Passwords does not match"]})

            instance.set_password(new_password)
            instance.save()

        profile = super(UserSerializer, self).update(instance, validated_data)
        return profile


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=False)
    profile_picture = serializers.ImageField(write_only=True, required=False)
    email = serializers.EmailField()
    phone = serializers.CharField(required=False)

    class Meta:
        model = UserProfile
        fields = ('phone', 'email', 'current_password', 'new_password', 'confirm_password', 'first_name', 'last_name', )
    
    def update(self, instance, validated_data):
        user_data = {
            'email': validated_data.get('email', instance.user.email),
            'profile_picture': validated_data.get('profile_picture', instance.user.profile_picture),
            'phone': validated_data.get('phone', instance.user.phone),
        }

        current_pass = helper.pop_key(validated_data, 'current_password')
        new_pass = helper.pop_key(validated_data, 'new_password')
        confirm_pass = helper.pop_key(validated_data, 'confirm_password')

        if current_pass and new_pass:
            if not confirm_pass:
                raise DotsValidationError({"confirm_password": ["Confirm Password is not provided"]})

            user_data['current_password'] = current_pass
            user_data['new_password'] = new_pass
            user_data['confirm_password'] = confirm_pass

        user = UserUpdateSerializer.update(UserUpdateSerializer(), instance=instance.user, validated_data=user_data)

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        instance.save()
        return instance


class ReturnUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'phone', 'role', 'profile_picture', 'stripe_id', )


class ReturnUserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'phone', 'profile_picture', 'stripe_id', 'updated_at', )


class ReturnSalonProfileSerializer(serializers.ModelSerializer):
    user = ReturnUserMeSerializer(required=True)

    class Meta:
        model = SalonProfile
        fields = ('user', 'salon_name', 'contact_name', )


class ReturnUserProfileSerializer(serializers.ModelSerializer):
    user = ReturnUserMeSerializer(required=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'first_name', 'last_name', 'referral_code', 'referrer', 'salon', 'stylist')


class ReturnShortUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'first_name', 'last_name', )


class ConfirmUserSerializer(serializers.Serializer):  # noqa
    token = serializers.CharField()


class ChangeStatusSerializer(serializers.Serializer):  # noqa
    status = serializers.ChoiceField(choices=Status.choices)


class ReferralUserSerializer(serializers.Serializer):
    referral_code = serializers.CharField()


def return_profile_serializer_by_role(user, context={}):
    if user.role == User.Role.ADMIN:
        return ReturnUserMeSerializer(user, context=context)
    elif user.role == User.Role.SALON:
        return ReturnSalonProfileSerializer(user.salon_profile, context=context)
    else:
        return ReturnUserProfileSerializer(user.profile, context=context)
