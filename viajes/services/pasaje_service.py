from ..models import Pasaje, Viaje
from ..utils.exceptions import BusinessError

class PasajeService:
    def listar_todos(self):
        return Pasaje.objects.filter(estado=True)

    def crear_pasaje(self, datos):
        viaje = datos.get('viaje')
        asiento = datos.get('numero_asiento')

        if Pasaje.objects.filter(viaje=viaje, numero_asiento__iexact=asiento).exists():
            raise BusinessError(f"El asiento '{asiento}' ya está reservado en este viaje.")

        capacidad = viaje.vehiculo.capacidad_asientos
        ocupados = Pasaje.objects.filter(viaje=viaje, estado=True).count()
        if ocupados >= capacidad:
            raise BusinessError("No hay más asientos disponibles en este viaje.")
        return Pasaje.objects.create(**datos)

    def actualizar_pasaje(self, instance, datos):
        viaje = datos.get('viaje', instance.viaje)
        asiento = datos.get('numero_asiento', instance.numero_asiento)

        if (asiento != instance.numero_asiento and
            Pasaje.objects.filter(viaje=viaje, numero_asiento__iexact=asiento).exclude(pk=instance.pk).exists()):
            raise BusinessError(f"El asiento '{asiento}' ya está reservado en este viaje.")

        if viaje != instance.viaje:
            capacidad = viaje.vehiculo.capacidad_asientos
            ocupados = Pasaje.objects.filter(viaje=viaje, estado=True).count()
            if ocupados >= capacidad:
                raise BusinessError("No hay más asientos disponibles en el nuevo viaje.")
        for attr, value in datos.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def eliminar_pasaje(self, instance):
        instance.delete()