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
                if request.method in ["POST", "PUT", "GET", "DELETE"]:
                    return True
                return False
            # Admin
            if request.user.is_superuser:
                return True

            if request.method in permissions.SAFE_METHODS:
                return True

        else:
            if request.method != "GET":
                return False
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
