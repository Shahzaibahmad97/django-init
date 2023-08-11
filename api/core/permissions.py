from django.contrib.contenttypes.models import ContentType
from rest_framework import permissions

from api.core.constants import DeviceType
from api.users.models import User


class IsAdmin(permissions.BasePermission):
    message = {'permission': ['You don\'t have permissions']}

    def has_permission(self, request, view):
        return getattr(request.user, 'is_superuser', False)


class IsUser(permissions.BasePermission):
    message = {'permission': ['You don\'t have permissions']}

    def has_permission(self, request, view):
        if not getattr(request.user, 'role', False):
            return False
        return request.user.role == User.Role.USER


class IsSalon(permissions.BasePermission):
    message = {'permission': ['You don\'t have permissions']}

    def has_permission(self, request, view):
        if not getattr(request.user, 'role', False):
            return False
        print(request.user.role)
        return request.user.role == User.Role.SALON.value


class RoleEqualToDeviceHeader(permissions.BasePermission):
    message = {'permission': ['Invalid login attempt']}

    def has_permission(self, request, view):
        device_type = request.headers.get('Device-Type', None)
        allowed_roles = {DeviceType.WEB: User.Role.USER, DeviceType.MOBILE: User.Role.USER}

        if allowed_roles[device_type] != request.user.role:
            return False

        return True


class ListPermission(permissions.BasePermission):
    message = {'permission': ['You don\'t have permissions']}

    def has_permission(self, request, view):
        ct = ContentType.objects.get_for_model(view.queryset.model)
        return request.user.has_perm(ct.app_label + '.view_' + ct.model)


class CreatePermission(permissions.BasePermission):
    message = {'permission': ['You don\'t have permissions']}

    def has_permission(self, request, view):
        ct = ContentType.objects.get_for_model(view.queryset.model)
        return request.user.has_perm(ct.app_label + '.add_' + ct.model)


class UpdatePermission(permissions.BasePermission):
    message = {'permission': ['You don\'t have permissions']}

    def has_permission(self, request, view):
        ct = ContentType.objects.get_for_model(view.queryset.model)
        return request.user.has_perm(ct.app_label + '.change_' + ct.model)


class DestroyPermission(permissions.BasePermission):
    message = {'permission': ['You don\'t have permissions']}

    def has_permission(self, request, view):
        ct = ContentType.objects.get_for_model(view.queryset.model)
        return request.user.has_perm(ct.app_label + '.delete_' + ct.model)
