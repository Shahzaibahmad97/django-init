from secrets import compare_digest

from rest_framework import serializers
from rest_framework.fields import empty

from api.core.constants import DeviceType
from api.core.utils import DotsValidationError
from api.core.validator import PasswordValidator
from api.jwtauth.serializers import UserCreateSerializer
from api.users.models import User


class BaseUserBuilderSerializer(serializers.ModelSerializer):
    device = None

    def to_representation(self, instance):
        instance = super().to_representation(instance)
        if self.context.get('step'):
            instance['register_step'] = self.context.get('step')
        return instance


class StepPersonalInformationSerializer(BaseUserBuilderSerializer):
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
        model = User
        fields = (
            'phone', 'email', 'current_password', 'confirm_password',
            'new_password', 'id'
        )

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

        profile = super(StepPersonalInformationSerializer, self).update(instance, validated_data)
        return profile


class StepRetrievePersonalInformationSerializer(BaseUserBuilderSerializer):
    class Meta:
        model = User
        fields = ('email', 'phone', )


class StepSerializer(serializers.Serializer):  # noqa
    step = serializers.ChoiceField(choices=User.RegisterSteps.choices)

    def validate(self, attrs):
        super(StepSerializer, self).validate(attrs)
        step_index = self.context['request'].user.steps.index(attrs['step'])
        user_step_index = self.context['request'].user.steps.index(self.context['request'].user.register_step)
        if step_index > user_step_index:
            raise serializers.ValidationError(
                {'step': f"Can not pass your current step: {self.context['request'].user.register_step}"}
            )

        return attrs
