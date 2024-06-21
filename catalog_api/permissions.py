from rest_framework import permissions

"""
Class IsAdminOrReadOnly restricts certain actions to admin users while allowing read-only access to everyone else.
"""


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
