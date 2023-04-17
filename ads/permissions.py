from rest_framework.permissions import BasePermission

from users.models import User


class IsOwner(BasePermission):
    message = "Редактировать/Удалять может только создатель подборки"

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "owner"):
            if request.user == obj.owner:
                return True
            return False
        if hasattr(obj, "author_id"):
            if request.user == obj.author_id:
                return True
            return False


class IsStaff(BasePermission):
    message = "Редактировать/Удалять может только  админ"

    def has_object_permission(self, request, view, obj):
        if request.user.role in [User.Roles.MODERATOR, User.Roles.ADMIN]:
            return True
        return False