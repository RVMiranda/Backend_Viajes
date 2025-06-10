from ..models import Pasajero, Pasaje
from ..utils.exceptions import BusinessError

class PasajeroService:
    def listar_todos(self):
        return Pasajero.objects.filter(estado=True)

    def crear_pasajero(self, datos):
        doc = datos.get('documento_identidad')
        if Pasajero.objects.filter(documento_identidad__iexact=doc).exists():
            raise BusinessError(f"Ya existe un pasajero con documento '{doc}'")
        return Pasajero.objects.create(**datos)

    def actualizar_pasajero(self, instance, datos):
        nuevo_doc = datos.get('documento_identidad', instance.documento_identidad)
        if Pasajero.objects.filter(documento_identidad__iexact=nuevo_doc).exclude(pk=instance.pk).exists():
            raise BusinessError(f"Otro pasajero ya usa el documento '{nuevo_doc}'")
        for attr, value in datos.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def eliminar_pasajero(self, instance):
        if Pasaje.objects.filter(pasajero=instance).exists():
            raise BusinessError("No se puede eliminar el pasajero con pasajes asociados.")
        instance.delete()
