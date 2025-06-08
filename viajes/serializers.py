from rest_framework import serializers
from .models import Rol, TipoTransporte, Usuario, Destino, Vehiculo, EstadoViaje, Pasajero, MetodoPago, EstatusPasaje, Viaje, Pasaje

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'

class TipoTransporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoTransporte
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class DestinoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destino
        fields = '__all__'

class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = '__all__'

class EstadoViajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoViaje
        fields = '__all__'

class PasajeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pasajero
        fields = '__all__'

class MetodoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetodoPago
        fields = '__all__'

class EstatusPasajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstatusPasaje
        fields = '__all__'

class ViajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Viaje
        fields = '__all__'

class PasajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pasaje
        fields = '__all__'
