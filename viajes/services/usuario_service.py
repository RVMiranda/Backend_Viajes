from ..models import Usuario
from ..utils.exceptions import BusinessError

class UsuarioService:
    def listar_todos(self):
        return Usuario.objects.filter(estado=True)

    def crear_usuario(self, datos):
        nombre = datos.get('nombre_usuario')
        if Usuario.objects.filter(nombre_usuario__iexact=nombre).exists():
            raise BusinessError(f"El nombre de usuario '{nombre}' ya está en uso.")
        usuario = Usuario.objects.create(**datos)
        return usuario

    def actualizar_usuario(self, instance, datos):
        nuevo_nombre = datos.get('nombre_usuario', instance.nombre_usuario)
        if Usuario.objects.filter(nombre_usuario__iexact=nuevo_nombre).exclude(pk=instance.pk).exists():
            raise BusinessError(f"El nombre de usuario '{nuevo_nombre}' ya está en uso.")
        for attr, value in datos.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def eliminar_usuario(self, instance):
        admin_role = Rol.objects.filter(nombre__iexact='Administrador').first()
        if instance.rol == admin_role:
            first_admin = Usuario.objects.filter(rol=admin_role).order_by('pk').first()
            if instance.pk == first_admin.pk:
                raise BusinessError("No se puede eliminar al primer administrador.")
        instance.delete()
