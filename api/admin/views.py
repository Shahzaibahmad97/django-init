from django.db.models import Count, Q, Prefetch, Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from api.categories.models import Category

from api.core.helper import date_range
import datetime
from api.admin.serializers import AdminProductImageSerializer, AdminUserSerializer, AdminProductTypeSerializer, AdminCategorySerializer, AdminVendorSerializer, AdminProductSerializer, ReturnAdminProductSerializer
from api.core.mixin import DotsModelViewSet, GenericDotsViewSet, RetrieveDotsModelMixin, DestroyDotsModelMixin, UpdateDotsModelMixin
from api.core.permissions import IsAdmin
from api.core.serializer import SuccessResponseSerializer
from api.core.utils import DotsValidationError
from api.product_types.models import ProductType
from api.products.models import Product, ProductImage
from api.users.models import User
from api.vendors.models import Vendor


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

    # @action(detail=True, methods=['GET'], serializer_class=StepPersonalInformationSerializer,
    #         url_path='personal-information')
    # def personal_information(self, request, *args, **kwargs):
    #     return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset()


class AdminCategoryViewSets(AdminModelViewSet):
    queryset = Category.objects.all()
    serializer_class = AdminCategorySerializer
    search_fields = ['name', ]
    filter_fields = ['name', ]


class AdminProductTypeViewSets(AdminModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = AdminProductTypeSerializer
    search_fields = ['name', ]
    filter_fields = ['name', ]


class AdminVendorViewSets(AdminModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = AdminVendorSerializer
    search_fields = ['name', ]
    filter_fields = ['name', ]


class AdminProductViewSets(AdminModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ReturnAdminProductSerializer
    serializer_create_class = AdminProductSerializer
    search_fields = ['title', 'short_description', 'category__name', ]
    filter_fields = ['title', 'short_description', 'category__name', 'product_type__name', 'vendor__name']

    def perform_create(self, serializer):
        serializer.validated_data['created_by'] = self.request.user
        return super().perform_create(serializer)


class AdminProductImageViewSet(AdminModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = AdminProductImageSerializer
    filter_fields = ['product_id']

