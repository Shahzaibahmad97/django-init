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


class ReturnProductListingSerializer(serializers.ModelSerializer):
    images = ReturnProductImageSerializer(many=True, read_only=True)
    category = ReturnCategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'short_description', 'reward_points', 'price', 'discounted_price', 'images', 'category']


class ReturnProductSerializer(serializers.ModelSerializer):
    images = ReturnProductImageSerializer(many=True, read_only=True)
    category = ReturnCategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'short_description', 'description', 'reward_points', 'price', 'discounted_price', 
                  'length', 'width', 'height', 'length_unit', 'weight', 'weight_unit', 'images', 'category']

