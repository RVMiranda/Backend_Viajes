from rest_framework import permissions

class IsAdminRole(permissions.BasePermission):
    """
    Sólo permite el acceso si request.user.rol.nombre == 'Administrador'
    """

    def has_permission(self, request, view):
        user = request.user
        return bool(user and getattr(user.rol, "nombre", "").lower() == "administrador")
