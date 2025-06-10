from ..models import EstatusPasaje, Pasaje
from ..utils.exceptions import BusinessError

class EstatusPasajeService:
    def listar_todos(self):
        return EstatusPasaje.objects.filter(estado=True)

    def crear_estatus(self, datos):
        desc = datos.get('descripcion')
        if EstatusPasaje.objects.filter(descripcion__iexact=desc).exists():
            raise BusinessError(f"El estatus '{desc}' ya existe.")
        return EstatusPasaje.objects.create(**datos)

    def actualizar_estatus(self, instance, datos):
        nueva_desc = datos.get('descripcion', instance.descripcion)
        if EstatusPasaje.objects.filter(descripcion__iexact=nueva_desc).exclude(pk=instance.pk).exists():
            raise BusinessError(f"Otro estatus con descripción '{nueva_desc}' ya existe.")
        instance.descripcion = nueva_desc
        instance.save()
        return instance

    def eliminar_estatus(self, instance):
        if Pasaje.objects.filter(estatus_pasaje=instance).exists():
            raise BusinessError("No se puede eliminar un estatus asignado a uno o más pasajes.")
        instance.delete()