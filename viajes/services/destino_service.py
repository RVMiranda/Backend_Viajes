from ..models import Destino, Viaje
from ..utils.exceptions import BusinessError

class DestinoService:
    """Lógica de negocio para gestión de Destinos."""
    def listar_todos(self):
        return Destino.objects.filter(estado=True)

    def crear_destino(self, datos):
        codigo = datos.get('codigo_terminal')
        if Destino.objects.filter(codigo_terminal__iexact=codigo).exists():
            raise BusinessError(f"El código terminal '{codigo}' ya existe.")
        return Destino.objects.create(**datos)

    def actualizar_destino(self, instance, datos):
        codigo_nuevo = datos.get('codigo_terminal', instance.codigo_terminal)
        if Destino.objects.filter(codigo_terminal__iexact=codigo_nuevo).exclude(pk=instance.pk).exists():
            raise BusinessError(f"El código terminal '{codigo_nuevo}' ya existe.")
        for attr, value in datos.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def eliminar_destino(self, instance):
        # No permitir eliminar destinos que tienen viajes asociados
        if Viaje.objects.filter(origen=instance).exists() or Viaje.objects.filter(destino=instance).exists():
            raise BusinessError("No se puede eliminar un destino asignado a uno o más viajes.")
        instance.delete()