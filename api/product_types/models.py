from django.db import models

from api.core.models import BaseModel


class ProductType(BaseModel):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        db_table = 'product_types'
