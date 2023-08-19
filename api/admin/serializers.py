from django.db.models import Avg
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from api.categories.models import Category
from api.product_types.models import ProductType
from api.products.models import Product, ProductImage

from api.users.models import User
from api.users.serializers import ReturnUserSerializer
from api.vendors.models import Vendor


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'phone', 'email', 'role', 'is_blocked', 'created_at'
        )


class AdminProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = '__all__'


class AdminCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AdminVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'


class AdminProductSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField(), required=True)

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        images_data = validated_data.pop('images', None)
        product = Product.objects.create(**validated_data)

        if images_data:
            for image_data in images_data:
                ProductImage.objects.create(product=product, image=image_data)

        return product

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', None)

        ProductImage.objects.filter(product=instance).delete()
        instance = super().update(instance, validated_data)

        if images_data:
            for image_data in images_data:
                ProductImage.objects.create(product=instance, image=image_data)

        return instance


class AdminProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ReturnAdminProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image')


class ReturnAdminProductSerializer(serializers.ModelSerializer):
    images = ReturnAdminProductImageSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = '__all__'


class ReplaceSerializer(serializers.Serializer):  # noqa
    item_id = serializers.IntegerField()
    message = serializers.CharField()

