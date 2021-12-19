from rest_framework import permissions


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """Проверка на авторизованного пользователя."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or request.user.is_authenticated
        )


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Проверка на автора."""

    def has_object_permission(self, request, view, obj):
        return (
            request.user == obj.author
        )

