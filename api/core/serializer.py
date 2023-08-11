from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.request import Request

from api.core.constants import DeviceType
from api.users.models import User
from api.users.builder_serializer import StepPersonalInformationSerializer

class OptionalFieldSerializer(serializers.Serializer):  # noqa
    name = serializers.CharField(max_length=100, required=True)
    required = serializers.BooleanField(default=True)
    label = serializers.CharField(required=True)


class SuccessResponseSerializer(serializers.Serializer):  # noqa
    success = serializers.BooleanField(default=True)
    message = serializers.CharField(label='success message')



class UserStepBuilderSerializer:
    serializers_by_step = None
    serializer = None
    request: Request = None

    def __init__(self, user_instance, data, step, request: Request):
        if step != User.RegisterSteps.PERSONAL_INFORMATION.value:
            self.data = data.copy()
            self.data.pop('step', None)
        else:
            self.data = data
        self.user_instance = user_instance
        self.step = step
        self.request = request

    def __call__(self, *args, **kwargs):
        if self.step == User.RegisterSteps.VERIFICATION.value:
            self.update_user_with_next_step(self.step)
            return None

        self.serializer = self.serializers_by_step[self.step](
            data=self.data,
            context={'step': self.user_instance.register_step, 'request': self.request}
        )
        if self.step != User.RegisterSteps.PERSONAL_INFORMATION:
            self.serializer.is_valid(raise_exception=True)
            return self.save_serializer()
        return self.save_serializer()

    def update_user_with_next_step(self, step):
        if self.user_instance.register_step == step:
            self.user_instance.register_step = self.user_instance.steps[self.user_instance.steps.index(step) + 1]
            self.user_instance.save()

    def save_serializer(self):
        step_function = getattr(self, f"patch_{self.step}")
        response = step_function()
        self.update_user_with_next_step(self.step)
        return response


class UserProfileBuilderSerializer(UserStepBuilderSerializer):
    serializers_by_step = {
        User.RegisterSteps.PERSONAL_INFORMATION: StepPersonalInformationSerializer,
    }

    def patch_personal_information(self):
        serializer = StepPersonalInformationSerializer(
            self.user_instance, self.data, partial=True,
            context={
                'request': self.request
            })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data
