from django.contrib import admin
from django.contrib.auth.models import Group
from django_rest_passwordreset.models import ResetPasswordToken

from api.users.models import User


@admin.register(User)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'phone', 'role',)
    search_fields = ('id', 'email', 'phone', 'role',)
    ordering = ('email',)


admin.site.unregister(Group)
admin.site.unregister(ResetPasswordToken)
