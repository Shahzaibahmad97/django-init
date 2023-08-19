from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import ListModelMixin

from api.core.mixin import GenericDotsViewSet
from api.product_types.models import ProductType
from api.product_types.serializers import ReturnProductTypeSerializer


class ProductTypeViewSet(GenericDotsViewSet, ListModelMixin):
    queryset = ProductType.objects.all()
    serializer_class = ReturnProductTypeSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

