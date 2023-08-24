from datetime import timedelta
from random import choice

from django.conf import settings
from django.db.models import Subquery, Prefetch, F, OuterRef, Exists, Q, Count, Avg, Case, When
from django.db.models.expressions import RawSQL
from django.utils import timezone
from django.utils.timezone import now
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.mixins import ListModelMixin
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from api.core.mixin import DotsModelViewSet, GenericDotsViewSet, ListDotsModelMixin, UpdateDotsModelMixin
from api.core.permissions import IsSalon, IsUser
from api.core.serializer import SuccessResponseSerializer
from api.core.utils import DotsValidationError
from api.jwtauth.helpers import send_confirmation_email
from api.users.models import SalonProfile, Stylist, StylistRequest, User, UserProfile
from api.users.serializers import ConfirmUserSerializer, ReferralUserSerializer, ReturnSalonProfileSerializer, ReturnShortUserProfileSerializer, ReturnUserMeSerializer, get_update_profile_serializer_class_by_role, get_return_profile_serializer_by_role, StylistRequestSerializer, ReturnStylistRequestSerializer, ReturnShortSalonProfileSerializer, StylistSerializer, ReturnStylistSerializer

user_confirmation_response = openapi.Response('User confirmation', SuccessResponseSerializer)


@swagger_auto_schema(method='PATCH')
@swagger_auto_schema(method='GET')
@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def partial_update(request):
    if request.method == 'PATCH':
        serializer_class = get_update_profile_serializer_class_by_role(request.user)
        serializer = serializer_class(instance=request.user.profile, data=request.data, context=dict(request=request), partial=True)
        serializer.is_valid(raise_exception=True)

        instance = serializer.save()
    
    serializer = get_return_profile_serializer_by_role(request.user, context=dict(request=request))
    return Response(serializer.data)


class UserViewSets(GenericDotsViewSet):
    serializer_class = ConfirmUserSerializer
    search_fields = []

    @swagger_auto_schema('DELETE', responses={200: user_confirmation_response})
    @action(detail=False, methods=['DELETE'],
            permission_classes=[IsAuthenticated])
    def delete(self, request, *args, **kwargs):
        request.user.delete()
        return Response(dict(success=True, message=f"User with email '{request.user.email}' is deleted", ))
    
    @action(detail=False, methods=['GET'], permission_classes=[AllowAny], serializer_class=ReferralUserSerializer)
    def referral(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.GET)
        serializer.is_valid(raise_exception=True)

        referrer = UserProfile.objects.filter(referral_code=serializer.validated_data['referral_code']).first()
        if not referrer:
            raise DotsValidationError({'referral_code': "Invalid referral code given."})
        
        return Response(ReturnShortUserProfileSerializer(instance=referrer).data)

    def get_queryset(self):
        # if self.request.user.is_anonymous:
        #     return User.objects.none()
        return super().get_queryset()


# salon related viewsets starts from here
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
    
    @action(detail=False, methods=['POST'], url_path='request-stylist/(?P<stylist_id>[0-9]+)',
        serializer_class=SuccessResponseSerializer, queryset=StylistRequest.objects.all(),
        permission_classes=[IsUser])
    def request_stylist(self, request, stylist_id, *args, **kwargs):
        stylist = get_object_or_404(Stylist, pk=stylist_id)
        
        if self.request.user.profile.salon_id != stylist.salon_id:
            raise DotsValidationError('Cannot select stylist from another salon. Please change your salon first.')
        if self.request.user.profile.stylist_id == stylist.id:
            raise DotsValidationError('Stylist already selected')
        
        StylistRequest.objects.create(stylist=stylist, salon_id=stylist.salon_id, created_by=self.request.user)
        return Response(SuccessResponseSerializer({'message': 'Stylist change request made successfully'}).data)

    def get_queryset(self):
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


class StylistChangeRequestViewSets(GenericDotsViewSet, ListModelMixin, UpdateDotsModelMixin):
    serializer_class = ReturnStylistRequestSerializer
    serializer_create_class = StylistRequestSerializer
    queryset = StylistRequest.objects.all().prefetch_related('stylist', 'stylist__salon', 'created_by')
    permission_classes = [IsSalon]
    filterset_fields = {
        'status': ['exact', 'in']
    }

    def perform_update(self, serializer):
        instance = super().perform_update(serializer)
        # assign the stylist to the user if the request is approved
        if instance.status == StylistRequest.Status.APPROVED:
            instance.created_by.profile.set_stylist(instance.stylist)

        return instance

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(stylist__salon__id=self.request.user.profile.id)
