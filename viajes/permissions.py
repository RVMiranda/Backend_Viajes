from rest_framework import permissions

class IsAdminRole(permissions.BasePermission):
    """
    Sólo permite el acceso si request.user.rol.nombre == 'Administrador'
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not hasattr(user, 'is_authenticated') or not user.is_authenticated:
            return False
        return getattr(user.rol, "nombre", "").lower() == "administrador"
