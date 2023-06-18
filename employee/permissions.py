from rest_framework import permissions


class EmployeeDirectoryUpdatePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_authenticated and obj.job_title != 'employee':
            return True
        return False
