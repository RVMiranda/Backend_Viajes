from ..models import EstadoViaje, Viaje
from ..utils.exceptions import BusinessError

class EstadoViajeService:
    def listar_todos(self):
        return EstadoViaje.objects.all()

    def crear_estado(self, datos):
        desc = datos.get('descripcion')
        if EstadoViaje.objects.filter(descripcion__iexact=desc).exists():
            raise BusinessError(f"El estado '{desc}' ya existe.")
        return EstadoViaje.objects.create(**datos)

    def actualizar_estado(self, instance, datos):
        nueva_desc = datos.get('descripcion', instance.descripcion)
        if EstadoViaje.objects.filter(descripcion__iexact=nueva_desc).exclude(pk=instance.pk).exists():
            raise BusinessError(f"Otro estado con descripción '{nueva_desc}' ya existe.")
        instance.descripcion = nueva_desc
        instance.save()
        return instance

    def eliminar_estado(self, instance):
        if Viaje.objects.filter(estado_viaje=instance).exists():
            raise BusinessError("No se puede eliminar un estado asociado a viajes.")
        instance.delete()