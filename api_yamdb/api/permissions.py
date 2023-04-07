"""Permissions module."""
from rest_framework import permissions


class AdminOrMyselfOnly(permissions.BasePermission):
    """
    Разрешение пользователям изменять свой профиль.

    У администраторов полный доступ.
    """

    def has_permission(self, request, view):
        """Has_permission func."""
        return request.user.is_authenticated and request.user.is_admin


class AdminOrReadOnly(permissions.BasePermission):
    """
    Разрешение "только для чтения" для всех.

    У администраторов полный доступ.
    """

    def has_permission(self, request, view):
        """Has_permission func."""
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated and request.user.is_admin
        )


class AdminOrModeratorOrAuthor(permissions.IsAuthenticatedOrReadOnly):
    """
    Разрешение пользователям управлять отзывами и комментариями.

    У администраторов и модераторов полный доступ.
    """

    def has_object_permission(self, request, view, obj):
        """Has_object_permission func."""
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (
                request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user
            )
        )
