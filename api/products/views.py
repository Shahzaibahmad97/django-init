from django.shortcuts import render

from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import ListModelMixin
from api.core.mixin import GenericDotsViewSet, RetrieveDotsModelMixin

from api.products.models import Product
from api.products.serializers import ReturnProductListingSerializer, ReturnProductSerializer


product_filterset_fields = {
        'created_at': ['gte', 'lte'],
        'title': ['iexact', 'contains'],
        'short_description': ['iexact', 'in'],
        'price': ['exact', 'gte', 'lte'],

        'category__name': ['exact', 'iexact'],
        'product_type__name': ['iexact'],
        'vendor__name': ['iexact'],
    }


class ProductViewSets(GenericDotsViewSet, RetrieveDotsModelMixin, ListModelMixin):
    queryset = Product.objects.all()
    serializer_class = ReturnProductListingSerializer
    filter_backends = GenericDotsViewSet.filter_backends + (filters.OrderingFilter, )
    ordering_fields = '__all__'
    search_fields = ['title', 'short_description', 'category__name', ]
    filterset_fields = product_filterset_fields
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.detail == True:
            return ReturnProductSerializer
        return super().get_serializer_class()
    
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

