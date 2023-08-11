from django.db.models import Count, Q, Prefetch, Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.core.helper import date_range
import datetime
from api.admin.serializers import AdminUserSerializer
from api.core.mixin import DotsModelViewSet, GenericDotsViewSet, RetrieveDotsModelMixin, DestroyDotsModelMixin
from api.core.permissions import IsAdmin
from api.core.serializer import SuccessResponseSerializer
from api.core.utils import DotsValidationError
from api.users.builder_serializer import StepPersonalInformationSerializer
from api.users.models import User


class AdminModelViewSet(DotsModelViewSet):
    permission_classes = [IsAdmin]
    filter_backends = (filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend)
    ordering_fields = '__all__'


class AdminUserViewSets(GenericDotsViewSet, ListModelMixin, RetrieveDotsModelMixin, DestroyDotsModelMixin):
    queryset = User.objects.exclude(is_superuser=True)
    serializer_class = AdminUserSerializer
    filter_backends = (filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend)
    permission_classes = [IsAdmin]
    search_fields = ['phone', 'email']
    filter_fields = ['is_blocked', 'role']
    ordering_fields = '__all__'

    @action(detail=True, methods=['POST'], url_path='block', queryset=User.objects.all(),
            serializer_create_class=SuccessResponseSerializer)
    def block(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_blocked = True
        user.save(update_fields=['is_blocked'])
        return Response({"success": True, "message": "User was successfully blocked"})

    @action(detail=True, methods=['POST'], url_path='unblock', queryset=User.objects.all(),
            serializer_create_class=SuccessResponseSerializer)
    def unblock(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_blocked = False
        user.save(update_fields=['is_blocked'])
        return Response({"success": True, "message": "User was successfully blocked"})

    @action(detail=True, methods=['GET'], serializer_class=StepPersonalInformationSerializer,
            url_path='personal-information')
    def personal_information(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset()

