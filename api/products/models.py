from decimal import Decimal
from django.db import models

from api.core.models import BaseModel, CreatedByModel, LengthUnits, WeightUnits
from api.core import fields

from api.categories.models import Category
from api.product_types.models import ProductType
from api.vendors.models import Vendor


class Product(BaseModel, CreatedByModel):
    title = models.CharField(max_length=100)
    short_description = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    price = fields.PositiveFloatField()

    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, related_name='products')
    product_type = models.ForeignKey(ProductType, null=True, on_delete=models.SET_NULL, related_name='products')
    vendor = models.ForeignKey(Vendor, default=1, null=True, on_delete=models.SET_NULL, related_name='products')

    length = models.FloatField(default=0)
    width = models.FloatField(default=0)
    height = models.FloatField(default=0)
    length_unit = models.CharField(max_length=5, choices=LengthUnits.choices, default=LengthUnits.FEET)

    weight = models.FloatField(default=0)
    weight_unit = models.CharField(max_length=5, choices=WeightUnits.choices, default=WeightUnits.OUNCES)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['id']
        db_table = 'products'
    
    @property
    def reward_points(self):
        return 250
    
    @property
    def discounted_price(self):
        return float(self.price) * 0.9


class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images')

    class Meta:
        ordering = ['id']
        db_table = 'product_images'

