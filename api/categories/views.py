from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import ListModelMixin

from api.core.mixin import GenericDotsViewSet
from api.categories.models import Category
from api.categories.serializers import ReturnCategorySerializer


class CategoryViewSet(GenericDotsViewSet, ListModelMixin):
    queryset = Category.objects.all()
    serializer_class = ReturnCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

