from django.shortcuts import render
from rest_framework import viewsets
from .models import Rol, TipoTransporte, Usuario, Destino, Vehiculo, EstadoViaje, Pasajero, MetodoPago, EstatusPasaje, Viaje, Pasaje
from .serializers import (
    RolSerializer, TipoTransporteSerializer, UsuarioSerializer, DestinoSerializer,
    VehiculoSerializer, EstadoViajeSerializer, PasajeroSerializer, MetodoPagoSerializer,
    EstatusPasajeSerializer, ViajeSerializer, PasajeSerializer
)

class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer

class TipoTransporteViewSet(viewsets.ModelViewSet):
    queryset = TipoTransporte.objects.all()
    serializer_class = TipoTransporteSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class DestinoViewSet(viewsets.ModelViewSet):
    queryset = Destino.objects.all()
    serializer_class = DestinoSerializer

class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer

class EstadoViajeViewSet(viewsets.ModelViewSet):
    queryset = EstadoViaje.objects.all()
    serializer_class = EstadoViajeSerializer

class PasajeroViewSet(viewsets.ModelViewSet):
    queryset = Pasajero.objects.all()
    serializer_class = PasajeroSerializer

class MetodoPagoViewSet(viewsets.ModelViewSet):
    queryset = MetodoPago.objects.all()
    serializer_class = MetodoPagoSerializer

class EstatusPasajeViewSet(viewsets.ModelViewSet):
    queryset = EstatusPasaje.objects.all()
    serializer_class = EstatusPasajeSerializer

class ViajeViewSet(viewsets.ModelViewSet):
    queryset = Viaje.objects.all()
    serializer_class = ViajeSerializer

class PasajeViewSet(viewsets.ModelViewSet):
    queryset = Pasaje.objects.all()
    serializer_class = PasajeSerializer

# Create your views here.
