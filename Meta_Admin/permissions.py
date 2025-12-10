

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешает безопасные методы (GET, HEAD, OPTIONS) всем,
    а изменять/удалять объект может только его владелец (obj.owner).
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return getattr(obj, "owner_id", None) == getattr(request.user, "id", None)
