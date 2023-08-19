from django.db import models

from api.core.models import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=190, unique=True)

    class Meta:
        db_table = 'product_categories'
