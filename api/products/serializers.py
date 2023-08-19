from rest_framework import serializers
from api.categories.serializers import ReturnCategorySerializer

from api.core.utils import DotsValidationError
from api.products.models import Product, ProductImage


class ReturnProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ReturnProductSerializer(serializers.ModelSerializer):
    images = ReturnProductImageSerializer(many=True, read_only=True)
    category = ReturnCategorySerializer(read_only=True)

    class Meta:
        model = Product
        exclude = ['updated_at', 'created_at', 'created_by']

