from django.utils import timezone
from datetime import timedelta
from ..models import Viaje
from ..utils.exceptions import BusinessError

class ViajeService:
    def listar_activos(self):
        return Viaje.objects.filter(estado=True)

    def crear_viaje(self, datos):
        # Validar lógica de negocio
        salida = datos.get('fecha_hora_salida')
        llegada = datos.get('fecha_hora_llegada')
        if llegada and llegada <= salida:
            raise BusinessError("La fecha de llegada debe ser posterior a la de salida.")
        # Crear
        viaje = Viaje.objects.create(**datos)
        return viaje

    def actualizar_viaje(self, instance, datos, partial=False):
        # Aplicar cambios y validaciones
        salida = datos.get('fecha_hora_salida', instance.fecha_hora_salida)
        llegada = datos.get('fecha_hora_llegada', instance.fecha_hora_llegada)
        if llegada and llegada <= salida:
            raise BusinessError("La fecha de llegada debe ser posterior a la de salida.")
        for attr, value in datos.items():
            setattr(instance, attr, value)
        instance.save()
        return instance