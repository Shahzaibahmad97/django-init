from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import ListModelMixin

from api.core.mixin import GenericDotsViewSet
from api.vendors.models import Vendor
from api.vendors.serializers import ReturnVendorSerializer


class VendorViewSet(GenericDotsViewSet, ListModelMixin):
    queryset = Vendor.objects.all()
    serializer_class = ReturnVendorSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

