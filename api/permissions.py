from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrReadOnly(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `author` attribute.
    """

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user


class PermissonForRole(BasePermission):
    """Object-level permission to only allow owners of an object to edit it.
    A
    ssumes the model instance has an `author` attribute.
    """

    def __init__(self, roles_permissions) -> None:
        super().__init__()
        self.roles_permissions = roles_permissions

    def has_permission(self, request, view):
        if hasattr(request.user, "role"):
            return (
                request.user.is_superuser
                or request.method
                in self.roles_permissions.get(request.user.role)
            )
        return False
