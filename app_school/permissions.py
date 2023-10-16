from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    message = 'Вы не являетесь модератором!'

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        else:
            return False
        # return request.user.groups.filter(is_staff=True).exists()


class IsOwner(BasePermission):
    message = 'Вы не являетесь владельцем!'

    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        return False
