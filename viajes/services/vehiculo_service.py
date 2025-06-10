from ..models import Vehiculo, Viaje
from ..utils.exceptions import BusinessError

class VehiculoService:
    """Lógica de negocio para gestión de Vehículos."""
    def listar_todos(self):
        return Vehiculo.objects.filter(estado=True)

    def crear_vehiculo(self, datos):
        matricula = datos.get('matricula')
        if Vehiculo.objects.filter(matricula__iexact=matricula).exists():
            raise BusinessError(f"Ya existe un vehículo con matrícula '{matricula}'")
        return Vehiculo.objects.create(**datos)

    def actualizar_vehiculo(self, instance, datos):
        matricula_nueva = datos.get('matricula', instance.matricula)
        if Vehiculo.objects.filter(matricula__iexact=matricula_nueva).exclude(pk=instance.pk).exists():
            raise BusinessError(f"Ya existe otro vehículo con matrícula '{matricula_nueva}'")
        for attr, value in datos.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def eliminar_vehiculo(self, instance):
        # No permitir eliminar si hay viajes asociados
        if Viaje.objects.filter(vehiculo=instance).exists():
            raise BusinessError("No se puede eliminar el vehículo porque está asignado a uno o más viajes.")
        instance.delete()