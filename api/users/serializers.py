from hmac import compare_digest
from rest_framework import serializers
from django.contrib.auth import get_user_model
from api.core.utils import DotsValidationError

from api.core.validator import PasswordValidator
from api.core.constants import Status
from api.core import helper
from api.salons.serializers import ReturnShortSalonProfileSerializer, ReturnStylistSerializer
from api.users.models import AdminProfile, Stylist, UserProfile, SalonProfile, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'


class UserUpdateSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True, required=False,
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
        print("***** hiiii ******")

        password = validated_data.pop('current_password', None)
        new_password = validated_data.pop('new_password', None)
        confirm_password = validated_data.pop('confirm_password', None)

        if password:
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

        profile = super().update(instance, validated_data)
        return profile


class AdminProfileUpdateSerializer(UserUpdateSerializer):
    profile_picture = serializers.ImageField(write_only=True, required=False)
    phone = serializers.CharField(required=False)

    class Meta:
        model = UserProfile
        fields = ('phone', 'email', 'current_password', 'new_password', 'confirm_password', 'profile_picture', 'fullname', )
    
    def update(self, instance, validated_data):
        instance.fullname = validated_data.get('fullname', instance.fullname)
        instance.user = UserUpdateSerializer.update(UserUpdateSerializer(), instance.user, validated_data)
        instance.save()
        return instance


class SalonProfileUpdateSerializer(UserUpdateSerializer):
    profile_picture = serializers.ImageField(write_only=True, required=False)
    phone = serializers.CharField(required=False)

    class Meta:
        model = UserProfile
        fields = ('phone', 'email', 'current_password', 'new_password', 'confirm_password', 'profile_picture', 'salon_name', 'contact_name', )
    
    def update(self, instance, validated_data):
        instance.salon_name = validated_data.get('salon_name', instance.salon_name)
        instance.contact_name = validated_data.get('contact_name', instance.contact_name)
        instance.user = UserUpdateSerializer.update(UserUpdateSerializer(), instance.user, validated_data)
        instance.save()
        return instance


class UserProfileUpdateSerializer(UserUpdateSerializer):
    profile_picture = serializers.ImageField(write_only=True, required=False)
    phone = serializers.CharField(required=False)

    class Meta:
        model = UserProfile
        fields = ('current_password', 'new_password', 'confirm_password', 'profile_picture', 'phone', 
                  'first_name', 'last_name', 'salon', 'stylist')
    
    def update(self, instance, validated_data):
        instance.first_name = validated_data.pop('first_name', instance.first_name)
        instance.last_name = validated_data.pop('last_name', instance.last_name)
        instance.salon = validated_data.pop('salon', instance.salon)
        instance.stylist = validated_data.pop('stylist', instance.stylist)
        instance.user = UserUpdateSerializer.update(UserUpdateSerializer(), instance.user, validated_data)
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


class ReturnAdminProfileSerializer(serializers.ModelSerializer):
    user = ReturnUserMeSerializer(required=True)

    class Meta:
        model = AdminProfile
        fields = ('user', 'fullname', )


class ReturnSalonProfileSerializer(serializers.ModelSerializer):
    user = ReturnUserMeSerializer(required=True)

    class Meta:
        model = SalonProfile
        fields = ('user', 'salon_name', 'contact_name', )


class ReturnUserProfileSerializer(serializers.ModelSerializer):
    user = ReturnUserMeSerializer(required=True)
    salon = ReturnShortSalonProfileSerializer()
    stylist = ReturnStylistSerializer()

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


def get_update_profile_serializer_class_by_role(user):
    if user.role == User.Role.ADMIN:
        return AdminProfileUpdateSerializer
    elif user.role == User.Role.SALON:
        return SalonProfileUpdateSerializer
    else:
        return UserProfileUpdateSerializer


def get_return_profile_serializer_by_role(user, context={}):
    if user.role == User.Role.ADMIN:
        return ReturnAdminProfileSerializer(user.profile, context=context)
    elif user.role == User.Role.SALON:
        return ReturnSalonProfileSerializer(user.profile, context=context)
    else:
        return ReturnUserProfileSerializer(user.profile, context=context)
