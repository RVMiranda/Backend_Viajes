from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
import uuid
from django.utils import timezone
from datetime import timedelta
from .models import Rol, TipoTransporte, Usuario, Destino, Vehiculo, EstadoViaje, Pasajero, MetodoPago, EstatusPasaje, Viaje, Pasaje, AuthToken
from .serializers import (
    RolSerializer, TipoTransporteSerializer, UsuarioSerializer, DestinoSerializer,
    VehiculoSerializer, EstadoViajeSerializer, PasajeroSerializer, MetodoPagoSerializer,
    EstatusPasajeSerializer, ViajeSerializer, PasajeSerializer
)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user = request.data.get("nombre_usuario")
        pwd  = request.data.get("contrasena")
        try:
            u = Usuario.objects.get(nombre_usuario=user, contrasena=pwd, estado=True)
        except Usuario.DoesNotExist:
            return Response({"detail": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)

        token_obj, created = AuthToken.objects.get_or_create(user=u,
            defaults={"expires": timezone.now() + timedelta(days=1)}
        )
        if not created and token_obj.expires < timezone.now():
            token_obj.token = uuid.uuid4().hex
            token_obj.expires = timezone.now() + timedelta(days=1)
            token_obj.save()

        return Response({"token": token_obj.token})

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
