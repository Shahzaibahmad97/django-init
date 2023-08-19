from django.db import models
from django.core.validators import MinValueValidator

from api.core.models import DecimalSizes


class PositiveFloatField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        kwargs['decimal_places'] = kwargs.get('decimal_places', DecimalSizes.Price.DECIMAL_PLACES)
        kwargs['max_digits'] = kwargs.get('max_digits', DecimalSizes.Price.MAX_DIGITS)
        kwargs['validators'] = kwargs.get('validators', [])
        kwargs['validators'].append(MinValueValidator(0))
        super().__init__(*args, **kwargs)
