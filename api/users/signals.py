import random
import string
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.contrib.auth import get_user_model

from api.payments.Stripe import Stripe
from api.users.models import UserProfile


@receiver(post_save, sender=get_user_model(), dispatch_uid='create_stripe_customer')
def create_stripe_customer(sender, instance, **kwargs):
    if instance.stripe_id == '':
        success, response = Stripe.create_customer(fullname=instance.name, cust_email=instance.email)
        if success:
            instance.stripe_id = response
            instance.save()
        else:
            raise Exception(response)


def generate_referral_code():
    alphabet_letters = random.sample(string.ascii_uppercase, 3)
    numeric_digits = random.sample(string.digits, 3)
    mixed_characters = [alphabet_letters[0], numeric_digits[0], alphabet_letters[1], numeric_digits[1], alphabet_letters[2], numeric_digits[2]]
    return ''.join(mixed_characters)


@receiver(post_save, sender=UserProfile, dispatch_uid='create_referral_code')
def create_referral_code(sender, instance, **kwargs):
    if instance.referral_code == '':
        referral_code = generate_referral_code()
        while UserProfile.objects.filter(referral_code=referral_code).exists():
            referral_code = generate_referral_code()
        instance.referral_code = referral_code
        instance.save()
 