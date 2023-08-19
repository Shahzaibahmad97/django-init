from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from api.core.mixin import GenericDotsViewSet, DotsModelViewSet, ListDotsModelMixin
from api.core.permissions import IsSalon
from api.salons.serializers import ReturnShortSalonProfileSerializer, ReturnStylistSerializer, StylistSerializer
from api.users.models import SalonProfile, Stylist
from api.users.serializers import ReturnSalonProfileSerializer


class SalonViewSets(DotsModelViewSet):
    serializer_class = ReturnSalonProfileSerializer
    queryset = SalonProfile.objects.all()
    search_fields = []
    permission_classes = [IsSalon]

    @action(detail=False, methods=['GET'], serializer_class=ReturnShortSalonProfileSerializer, queryset=SalonProfile.objects.all(),
            permission_classes=[AllowAny])
    def get_salons(self, request, *args, **kwargs):
        return ListDotsModelMixin.list_dropdown(self, request, *args, **kwargs)

    @action(detail=True, methods=['GET'], url_path='stylist',
            serializer_class=ReturnStylistSerializer, queryset=SalonProfile.objects.all(),
            permission_classes=[AllowAny])
    def get_salon_stylists(self, request, pk, *args, **kwargs):
        salon = get_object_or_404(SalonProfile, pk=pk)
        self.queryset = salon.stylists.all()
        return ListDotsModelMixin.list_dropdown(self, request, *args, **kwargs)

    def get_queryset(self):
        # if self.request.user.is_anonymous:
        #     return User.objects.none()
        return super().get_queryset()


class StylistViewSets(DotsModelViewSet):
    serializer_class = ReturnStylistSerializer
    serializer_create_class = StylistSerializer
    queryset = Stylist.objects.all()
    permission_classes = [IsSalon]

    def perform_create(self, serializer):
        serializer.validated_data['salon'] = self.request.user.profile
        return super().perform_create(serializer)

    def get_queryset(self):
        queryset = super().get_queryset()
        
        return queryset.filter(salon_id=self.request.user.profile.id)
