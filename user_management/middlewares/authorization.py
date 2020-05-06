from rest_framework import permissions


class CentralAuthorization(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return (None, None)
