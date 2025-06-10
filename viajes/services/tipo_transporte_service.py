from ..models import TipoTransporte
from ..utils.exceptions import BusinessError

class TipoTransporteService:
    def listar_todos(self):
        return TipoTransporte.objects.all()

    def crear_tipo_transporte(self, datos):
        nombre = datos.get('nombre')
        if TipoTransporte.objects.filter(nombre__iexact=nombre).exists():
            raise BusinessError(f"Ya existe un tipo de transporte con nombre '{nombre}'")
        tipo = TipoTransporte.objects.create(**datos)
        return tipo

    def actualizar_tipo_transporte(self, instance, datos):
        nombre = datos.get('nombre', instance.nombre)
        if TipoTransporte.objects.filter(nombre__iexact=nombre).exclude(pk=instance.pk).exists():
            raise BusinessError(f"Ya existe otro tipo de transporte con nombre '{nombre}'")
        for attr, value in datos.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def eliminar_tipo_transporte(self, instance):
        instance.delete()
        return None