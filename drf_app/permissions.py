from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsModerator(permissions.BasePermission):
    message = 'Вы не являетесь модератором!'

    def has_permission(self, request, view):
        if request.user.groups.filter(name='Модераторы').exists():
            return True
        else:
            self.message = 'Вы не являетесь модератором!'
            return False


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'user'):
            if obj.user == request.user:
                return True
            else:
                raise PermissionDenied("Вы не являетесь владельцем этого объекта.")
        raise PermissionDenied("У вас нет доступа к этому объекту.")

