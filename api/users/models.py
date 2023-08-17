from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.timezone import now
from django.utils.translation import gettext as _
from api.core.helper import get_file_path

from api.core.managers import CustomUserManager
from api.users.helper import generate_code


class User(AbstractBaseUser, PermissionsMixin):
    class RegisterSteps(models.TextChoices):
        PERSONAL_INFORMATION = 'personal_information', _('personal_information')
        VERIFICATION = 'verification', _('Verification')
        COMPLETED = 'completed', _('completed')

    USER_STEPS = [
        RegisterSteps.PERSONAL_INFORMATION,
        RegisterSteps.VERIFICATION,
        RegisterSteps.COMPLETED,
    ]

    class Role(models.TextChoices):
        USER = 'user', _('User')
        SALON = 'salon', _('Salon')
        ADMIN = 'admin', _('Admin')

    USERNAME_FIELD = 'email'
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=190, unique=True)
    
    role = models.CharField(max_length=100, default=Role.USER.value, choices=Role.choices)

    profile_picture = models.ImageField(upload_to=get_file_path, default=settings.DEFAULT_PROFILE_IMAGE)

    fcm_token = models.TextField(blank=True)
    stripe_id = models.CharField(max_length=100, blank=True, default='')

    is_staff = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=now, null=True)

    objects = CustomUserManager()

    @property
    def name(self):
        try:
            if self.role == User.Role.ADMIN:
                return self.admin_profile.fullname
            elif self.role == User.Role.SALON:
                return self.salon_profile.salon_name
            else:
                return self.profile.name
        except Exception as ex:
            print("No name: ", ex)
            return ""
    
    @property
    def my_profile(self):
        try:
            if self.role == User.Role.ADMIN:
                return self.admin_profile
            elif self.role == User.Role.SALON:
                return self.salon_profile
            else:
                return self.profile
        except Exception as ex:
            print("No profile created yet: ", ex)
            return None

    @property
    def picture(self):
        return self.profile_picture.url

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['id']
        db_table = 'users'


class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')

    fullname = models.CharField(max_length=150, blank=True, default="")

    @property
    def name(self):
        return self.fullname


class SalonProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='salon_profile')

    salon_name = models.CharField(max_length=190)
    contact_name = models.CharField(max_length=190)

    @property
    def name(self):
        return self.salon_name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    first_name = models.CharField(max_length=190)
    last_name = models.CharField(max_length=190)

    referral_code = models.CharField(max_length=6)

    referrer = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)
    salon = models.ForeignKey(SalonProfile, on_delete=models.SET_NULL, null=True)
    stylist = models.ForeignKey("Stylist", on_delete=models.SET_NULL, null=True)

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"


class Stylist(models.Model):
    salon = models.ForeignKey(SalonProfile, on_delete=models.CASCADE, related_name='stylists')

    fullname = models.CharField(max_length=150)
