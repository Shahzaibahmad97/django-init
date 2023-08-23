from django.db import models
from django.utils.translation import gettext as _

from api.core.models import BaseModel, CharFieldSizes
from api.users.models import User


class Reward(BaseModel):
    class Types(models.TextChoices):
        PURCHASE = 'purchase', _('Purchase Reward')
        REFERRAL = 'referral', _('Referral Reward')

    points = models.PositiveSmallIntegerField()

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='rewards')
    reward_type = models.CharField(max_length=CharFieldSizes.EXTRA_SMALL, choices=Types.choices, default=Types.PURCHASE)

    class Meta:
        ordering = ['user']
        db_table = 'rewards'
