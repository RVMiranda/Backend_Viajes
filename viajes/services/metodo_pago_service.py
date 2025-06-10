from ..models import MetodoPago, Pasaje
from ..utils.exceptions import BusinessError

class MetodoPagoService:
    def listar_todos(self):
        return MetodoPago.objects.filter(estado=True)

    def crear_metodo_pago(self, datos):
        desc = datos.get('descripcion')
        if MetodoPago.objects.filter(descripcion__iexact=desc).exists():
            raise BusinessError(f"El método de pago '{desc}' ya existe.")
        return MetodoPago.objects.create(**datos)

    def actualizar_metodo_pago(self, instance, datos):
        nueva_desc = datos.get('descripcion', instance.descripcion)
        if MetodoPago.objects.filter(descripcion__iexact=nueva_desc).exclude(pk=instance.pk).exists():
            raise BusinessError(f"Otro método de pago con descripción '{nueva_desc}' ya existe.")
        instance.descripcion = nueva_desc
        instance.save()
        return instance

    def eliminar_metodo_pago(self, instance):
        if Pasaje.objects.filter(metodo_pago=instance).exists():
            raise BusinessError("No se puede eliminar el método de pago asignado a uno o más pasajes.")
        instance.delete()