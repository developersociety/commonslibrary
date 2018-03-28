from rest_framework import permissions


class ResourcePermission(permissions.BasePermission):
    message = 'Updating resource for like not allowed for anonymous users.'

    def has_permission(self, request, view):
        if request.method == 'PUT' and request.user.is_authenticated():
            allowed = True
        elif request.method == 'GET':
            allowed = True
        else:
            allowed = False
        return allowed
