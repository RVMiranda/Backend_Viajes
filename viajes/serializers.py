from rest_framework import serializers
from .models import Rol, TipoTransporte, Usuario, Destino, Vehiculo, EstadoViaje, Pasajero, MetodoPago, EstatusPasaje, Viaje, Pasaje

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = [ 'id', 'nombre']

class TipoTransporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoTransporte
        fields = ['id', 'nombre','descripcion']

class UsuarioSerializer(serializers.ModelSerializer):
    rol = RolSerializer(read_only=True)
    rol_id = serializers.PrimaryKeyRelatedField(
        queryset=Rol.objects.all(), source='rol', write_only=True
    )
    class Meta:
        model = Usuario
        fields = [
            'id',
            'nombre_usuario',
            'contrasena',
            'rol',
            'rol_id',
            'fecha_creacion',
            'fecha_actualizacion',
            'estado',
        ]
        read_only_fields = ['rol','fecha_creacion', 'fecha_actualizacion']

class DestinoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destino
        fields = [
            'id',
            'ciudad',
            'pais',
            'codigo_terminal',
            'fecha_creacion',
            'fecha_actualizacion',
            'estado',
        ]
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion']

class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = [
            'id',
            'tipo_transporte',       
            'capacidad_asientos',   
            'matricula',            
            'fecha_creacion',
            'fecha_actualizacion',
            'estado',                
        ]
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion']

class EstadoViajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoViaje
        fields = ['id', 'descripcion']

class PasajeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pasajero
        fields = [
            'id',
            'nombre_completo',
            'documento_identidad',
            'correo_electronico',
            'telefono',
            'fecha_creacion',
            'fecha_actualizacion',
            'estado',
        ]
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion']

class MetodoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetodoPago
        fields = [
            'id',
            'descripcion',
            'fecha_creacion',
            'fecha_actualizacion',
            'estado',
        ]
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion']

class EstatusPasajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstatusPasaje
        fields = [
            'id',
            'descripcion',
            'fecha_creacion',
            'fecha_actualizacion',
            'estado',
        ]
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion']

class ViajeSerializer(serializers.ModelSerializer):
    origen = DestinoSerializer(read_only=True)
    destino = DestinoSerializer(read_only=True)
    vehiculo = VehiculoSerializer(read_only=True)
    estado_viaje = EstadoViajeSerializer(read_only=True)

    origen_id = serializers.PrimaryKeyRelatedField(
        queryset=Destino.objects.all(), source='origen', write_only=True
    )
    destino_id = serializers.PrimaryKeyRelatedField(
        queryset=Destino.objects.all(), source='destino', write_only=True
    )
    vehiculo_id = serializers.PrimaryKeyRelatedField(
        queryset=Vehiculo.objects.all(), source='vehiculo', write_only=True
    )
    estado_viaje_id = serializers.PrimaryKeyRelatedField(
        queryset=EstadoViaje.objects.all(), source='estado_viaje', write_only=True
    )

    class Meta:
        model = Viaje
        fields = [
            'id',
            'origen', 'origen_id',
            'destino', 'destino_id',
            'vehiculo', 'vehiculo_id',
            'fecha_hora_salida',
            'fecha_hora_llegada',
            'precio_base',
            'estado_viaje', 'estado_viaje_id',
            'fecha_creacion',
            'fecha_actualizacion',
            'estado',
        ]
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion']

class PasajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pasaje
        fields = [
            'id',
            'viaje',            
            'pasajero',         
            'numero_asiento',   
            'precio_pagado',    
            'estatus_pasaje',   
            'metodo_pago',      
            'fecha_compra',     
            'usuario_compra',   
            'fecha_creacion',
            'fecha_actualizacion',
            'estado',           
        ]
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion']
