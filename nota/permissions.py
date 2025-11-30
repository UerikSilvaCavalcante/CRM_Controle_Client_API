from rest_framework import permissions


class IsAdminOrVendedorOwner(permissions.BasePermission):
    """
    Permisão custumizado para o usuario do tipo vendedor ou admin
    - Admin: acesso total
    - Vendedor: acesso aos seus clientes e as notas dele
    - Outros: apenas visualização de suas notas
    """

    def has_permission(self, request, view):  # type: ignore
        if not isinstance(request.user, str):

            if not request.user.is_authenticated:
                return False

            # Vendedor
            if request.user.groups.filter(name="Vendedor").exists():
                return True

            # Admin
            if request.user.is_superuser:
                return True

            if request.method in permissions.SAFE_METHODS:
                return True
        else:
            return True

        return False

    def has_object_permission(self, request, view, obj):  # type: ignore

        if request.user.groups.filter(name="Vendedor").exists():
            if hasattr(obj, "usuario"):
                return obj.usuario == request.user
            return False

        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        return False


class IsAdminGroup(permissions.BasePermission):
    """
    Apenas usuários do grupo 'admin' têm acesso
    Útil para views de criação de usuários
    """

    def has_permission(self, request, view):  # type: ignore
        if not request.user.is_authenticated:
            return False

        return request.user.groups.filter(name="admin").exists()
