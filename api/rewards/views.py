from django.shortcuts import render

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin

from api.core.mixin import GenericDotsViewSet
from api.core.permissions import IsUser
from api.rewards.serializers import ReturnRewardsSerializer


class RewardViewSets(GenericDotsViewSet, ListModelMixin):
    serializer_class = ReturnRewardsSerializer
    permission_classes = [IsUser]

    def list(self, request, *args, **kwargs):
        data = {'total_points': 750, 'free_products': 3}
        serializer = ReturnRewardsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    def get_queryset(self):
        return super().get_queryset()
