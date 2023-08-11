from django.db.models import Avg
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.users.models import User
from api.users.serializers import ReturnUserSerializer


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'phone', 'email', 'role', 'is_blocked', 'created_at'
        )


class ReplaceSerializer(serializers.Serializer):  # noqa
    item_id = serializers.IntegerField()
    message = serializers.CharField()

