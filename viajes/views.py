from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
import uuid
from django.utils import timezone
from datetime import timedelta
# imports de archivos del proyecto
from .models import Rol, TipoTransporte, Usuario, Destino, Vehiculo, EstadoViaje, Pasajero, MetodoPago, EstatusPasaje, Viaje, Pasaje, AuthToken
from .serializers import (
    RolSerializer, TipoTransporteSerializer, UsuarioSerializer, DestinoSerializer,
    VehiculoSerializer, EstadoViajeSerializer, PasajeroSerializer, MetodoPagoSerializer,
    EstatusPasajeSerializer, ViajeSerializer, PasajeSerializer
)
from .authentication import TokenAuthentication
from .permissions import IsAdminRole
from .services.viaje_service import ViajeService
from .utils.exceptions import BusinessError
from .services.rol_service import RolService
from .services.tipo_transporte_service import TipoTransporteService
from .services.usuario_service import UsuarioService

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
    authentication_classes = [TokenAuthentication]
    permission_classes     = [IsAdminRole]
    service = RolService()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            rol = self.service.crear_rol(serializer.validated_data)
        except BusinessError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        out = self.get_serializer(rol)
        return Response(out.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            rol = self.service.actualizar_rol(instance, serializer.validated_data)
        except BusinessError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(rol).data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.service.eliminar_rol(instance)
        except BusinessError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)

class TipoTransporteViewSet(viewsets.ModelViewSet):
    queryset = TipoTransporte.objects.all()
    serializer_class = TipoTransporteSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes     = [IsAdminRole]
    service = TipoTransporteService()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            tipo = self.service.crear_tipo_transporte(serializer.validated_data)
        except BusinessError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(tipo).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            tipo = self.service.actualizar_tipo_transporte(instance, serializer.validated_data)
        except BusinessError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(tipo).data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.service.eliminar_tipo_transporte(instance)
        except BusinessError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes     = [IsAdminRole]
    service = UsuarioService()

    def retrieve(self, request, *args, **kwargs):
        usuario = self.get_object()
        serializer = self.get_serializer(usuario)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            usuario = self.service.crear_usuario(serializer.validated_data)
        except BusinessError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(usuario).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            usuario = self.service.actualizar_usuario(instance, serializer.validated_data)
        except BusinessError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(usuario).data)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            usuario = self.service.actualizar_usuario(instance, serializer.validated_data)
        except BusinessError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(usuario).data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.service.eliminar_usuario(instance)
        except BusinessError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)

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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminRole]
    service = ViajeService()

    def list(self, request):
        viajes = self.service.listar_activos()
        serializer = ViajeSerializer(viajes, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        viaje = self.service.listar_activos().filter(pk=pk).first()
        if not viaje:
            return Response({'detail': 'No encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ViajeSerializer(viaje)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = ViajeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        try:
            viaje = self.service.crear_viaje(data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except BusinessError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        out = ViajeSerializer(viaje)
        return Response(out.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        instance = self.service.listar_activos().filter(pk=pk).first()
        if not instance:
            return Response({'detail': 'No encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ViajeSerializer(instance, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        datos = serializer.validated_data
        try:
            viaje = self.service.actualizar_viaje(instance, datos)
        except BusinessError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(ViajeSerializer(viaje).data)
    
    def destroy(self, request, pk=None):
        instance = self.service.listar_activos().filter(pk=pk).first()
        if not instance:
            return Response({'detail': 'No encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def partial_update(self, request, pk=None):
        instance = self.service.listar_activos().filter(pk=pk).first()
        if not instance:
            return Response({'detail': 'No encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ViajeSerializer(instance, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        datos = serializer.validated_data
        try:
            viaje = self.service.actualizar_viaje(instance, datos, partial=True)
        except BusinessError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(ViajeSerializer(viaje).data)

class PasajeViewSet(viewsets.ModelViewSet):
    queryset = Pasaje.objects.all()
    serializer_class = PasajeSerializer

# Create your views here.
