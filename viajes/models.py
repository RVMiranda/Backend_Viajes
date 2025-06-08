from django.db import models
#para cargar los datos basicos de la base de datos:
# docker-compose exec web python manage.py loaddata initial_data.json

#para crear alguna migracion:
# docker-compose exec web python manage.py makemigrations viajes

# para aplicar las migraciones:
# docker-compose exec web python manage.py migrate viajes

# Create your models here.
class Rol(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class TipoTransporte(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.descripcion


class Usuario(models.Model):
    nombre_usuario = models.CharField(max_length=150, unique=True)
    contrasena = models.CharField(max_length=128)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT, related_name='usuarios')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario_creacion = models.ForeignKey(
        'self', null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='creados_por'
    )
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    usuario_actualizacion = models.ForeignKey(
        'self', null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='actualizados_por'
    )
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_usuario


class Destino(models.Model):
    ciudad = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    codigo_terminal = models.CharField(max_length=50)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario_creacion = models.ForeignKey(
        Usuario, null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='destinos_creados'
    )
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    usuario_actualizacion = models.ForeignKey(
        Usuario, null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='destinos_actualizados'
    )
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.ciudad} - {self.pais}"


class Vehiculo(models.Model):
    tipo_transporte = models.ForeignKey(
        TipoTransporte, on_delete=models.PROTECT,
        related_name='vehiculos'
    )
    capacidad_asientos = models.PositiveIntegerField()
    matricula = models.CharField(max_length=50)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario_creacion = models.ForeignKey(
        Usuario, null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='vehiculos_creados'
    )
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    usuario_actualizacion = models.ForeignKey(
        Usuario, null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='vehiculos_actualizados'
    )
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.matricula


class EstadoViaje(models.Model):
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.descripcion


class Pasajero(models.Model):
    nombre_completo = models.CharField(max_length=200)
    documento_identidad = models.CharField(max_length=50)
    correo_electronico = models.EmailField()
    telefono = models.CharField(max_length=20)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario_creacion = models.ForeignKey(
        Usuario, null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='pasajeros_creados'
    )
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    usuario_actualizacion = models.ForeignKey(
        Usuario, null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='pasajeros_actualizados'
    )
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_completo


class MetodoPago(models.Model):
    descripcion = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario_creacion = models.ForeignKey(
        Usuario, null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='metodos_creados'
    )
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    usuario_actualizacion = models.ForeignKey(
        Usuario, null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='metodos_actualizados'
    )
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.descripcion


class EstatusPasaje(models.Model):
    descripcion = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario_creacion = models.ForeignKey(
        Usuario, null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='estatus_creados'
    )
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    usuario_actualizacion = models.ForeignKey(
        Usuario, null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='estatus_actualizados'
    )
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.descripcion


class Viaje(models.Model):
    origen = models.ForeignKey(
        Destino, on_delete=models.PROTECT,
        related_name='viajes_origen'
    )
    destino = models.ForeignKey(
        Destino, on_delete=models.PROTECT,
        related_name='viajes_destino'
    )
    vehiculo = models.ForeignKey(
        Vehiculo, on_delete=models.PROTECT,
        related_name='viajes'
    )
    fecha_hora_salida = models.DateTimeField()
    fecha_hora_llegada = models.DateTimeField(null=True, blank=True)
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    estado_viaje = models.ForeignKey(
        EstadoViaje, on_delete=models.PROTECT,
        related_name='viajes'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario_creacion = models.ForeignKey(
        Usuario, null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='viajes_creados'
    )
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    usuario_actualizacion = models.ForeignKey(
        Usuario, null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='viajes_actualizados'
    )
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f"Viaje {self.id}: {self.origen} → {self.destino}"  


class Pasaje(models.Model):
    viaje = models.ForeignKey(
        Viaje, on_delete=models.CASCADE,
        related_name='pasajes'
    )
    pasajero = models.ForeignKey(
        Pasajero, on_delete=models.CASCADE,
        related_name='pasajes'
    )
    numero_asiento = models.CharField(max_length=10)
    precio_pagado = models.DecimalField(max_digits=10, decimal_places=2)
    estatus_pasaje = models.ForeignKey(
        EstatusPasaje, on_delete=models.PROTECT,
        related_name='pasajes'
    )
    metodo_pago = models.ForeignKey(
        MetodoPago, on_delete=models.PROTECT,
        related_name='pasajes'
    )
    fecha_compra = models.DateTimeField()
    usuario_compra = models.ForeignKey(
        Usuario, null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='compras_pasajes'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario_creacion = models.ForeignKey(
        Usuario, null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='pasajes_creados'
    )
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    usuario_actualizacion = models.ForeignKey(
        Usuario, null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='pasajes_actualizados'
    )
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f"Pasaje {self.id} - Asiento {self.numero_asiento}"