from ..models import Rol
from ..utils.exceptions import BusinessError

class RolService:
    """Lógica de negocio para gestión de Roles."""
    def listar_todos(self):
        return Rol.objects.all()

    def crear_rol(self, datos):
        nombre = datos.get('nombre')
        if Rol.objects.filter(nombre__iexact=nombre).exists():
            raise BusinessError(f"Ya existe un rol con nombre '{nombre}'")
        rol = Rol.objects.create(**datos)
        return rol

    def actualizar_rol(self, instance, datos):
        nombre = datos.get('nombre', instance.nombre)
        if Rol.objects.filter(nombre__iexact=nombre).exclude(pk=instance.pk).exists():
            raise BusinessError(f"Ya existe otro rol con nombre '{nombre}'")
        instance.nombre = nombre
        instance.save()
        return instance

    def eliminar_rol(self, instance):
        instance.delete()
        return None