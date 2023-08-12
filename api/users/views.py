from datetime import timedelta
from random import choice

from django.conf import settings
from django.db.models import Subquery, Prefetch, F, OuterRef, Exists, Q, Count, Avg, Case, When
from django.db.models.expressions import RawSQL
from django.utils import timezone
from django.utils.timezone import now
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from api.core.constants import DeviceType, Status
from api.core.mixin import GenericDotsViewSet, ListDotsModelMixin
from api.core.serializer import SuccessResponseSerializer, UserProfileBuilderSerializer
from api.core.utils import DotsValidationError
from api.jwtauth.helpers import send_confirmation_email
from api.users.models import SalonProfile, Stylist, User, UserProfile
from api.users.serializers import ConfirmUserSerializer, ReferralUserSerializer, ReturnShortUserProfileSerializer, ReturnUserMeSerializer, return_profile_serializer_by_role

user_confirmation_response = openapi.Response('User confirmation', SuccessResponseSerializer)


@swagger_auto_schema(method='PATCH')
@swagger_auto_schema(method='GET')
@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def partial_update(request):
    print(request)
    if request.method == 'PATCH':
        # profile_completed = request.user.is_completed
        # serializer = StepSerializer(data=request.data, context=dict(request=request))
        # serializer.is_valid(raise_exception=True)
        # builder_serializer_class = UserProfileBuilderSerializer

        # builder_serializer = builder_serializer_class(
        #     user_instance=request.user,
        #     data=request.data,
        #     step=serializer.validated_data['step'],
        #     request=request
        # )
        # response = builder_serializer()

        if response is None:
            response = dict(
                success=True,
                message=f"step successfully updated to "  # noqa
            )

        return Response(response)

    serializer = return_profile_serializer_by_role(request.user, context=dict(request=request))
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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        referrer = UserProfile.objects.filter(referral_code=serializer.validated_data['referral_code']).first()
        if not referrer:
            raise DotsValidationError({'referral_code': "Invalid referral code given."})
        
        return Response(ReturnShortUserProfileSerializer(instance=referrer).data)

    def get_queryset(self):
        # if self.request.user.is_anonymous:
        #     return User.objects.none()
        return super().get_queryset()

