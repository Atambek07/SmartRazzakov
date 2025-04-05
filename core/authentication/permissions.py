from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsMunicipalWorker(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='municipal_workers').exists()

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user

class CitizenAccessPermission(BasePermission):
    """
    Grants full access to municipal workers, read-only to citizens
    """
    def has_permission(self, request, view):
        if request.user.groups.filter(name='municipal_workers').exists():
            return True
        return request.method in SAFE_METHODS