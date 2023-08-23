from django.db import models

from api.core.models import BaseModel, CharFieldSizes, CreatedByModel


class ContactUs(BaseModel, CreatedByModel):
    name = models.CharField(max_length=CharFieldSizes.MEDIUM)
    email = models.EmailField(max_length=CharFieldSizes.LARGE)
    message = models.CharField(max_length=CharFieldSizes.MAX)

    class Meta:
        ordering = ['id']
        db_table = 'contact_us'


class Feedback(BaseModel, CreatedByModel):
    message = models.CharField(max_length=CharFieldSizes.MAX)

    class Meta:
        ordering = ['id']
        db_table = 'feedbacks'
