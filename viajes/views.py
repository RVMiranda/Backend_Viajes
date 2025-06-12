from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
import uuid
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import TruncMonth
from django.db.models import Count
# imports de archivos del proyecto
from .models import Rol, TipoTransporte, Usuario, Destino, Vehiculo, EstadoViaje, Pasajero, MetodoPago, EstatusPasaje, Viaje, Pasaje, AuthToken
from .serializers import (
    RolSerializer, TipoTransporteSerializer, UsuarioSerializer, DestinoSerializer,
    VehiculoSerializer, EstadoViajeSerializer, PasajeroSerializer, MetodoPagoSerializer,
    EstatusPasajeSerializer, ViajeSerializer, PasajeSerializer
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .authentication import TokenAuthentication
from .permissions import IsAdminRole
from .services.viaje_service import ViajeService
from .utils.exceptions import BusinessError
from .services.rol_service import RolService
from .services.tipo_transporte_service import TipoTransporteService
from .services.usuario_service import UsuarioService
from .services.destino_service import DestinoService
from .services.vehiculo_service import VehiculoService
from .services.estado_viaje_service import EstadoViajeService
from .services.pasajero_service import PasajeroService
from .services.metodo_pago_service import MetodoPagoService
from .services.estatus_pasaje_service import EstatusPasajeService
from .services.pasaje_service import PasajeService

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
    service = TipoTransporteService()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdminRole()]

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

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nombre_usuario']

    def get_permissions(self):
        if self.action in ['create', 'lookup', 'partial_update']:
            return [AllowAny()]
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdminRole()]

    @action(detail=False, methods=['get'], url_path='lookup')
    def lookup(self, request):
        nombre = request.query_params.get('nombre_usuario')
        if not nombre:
            return Response({'detail': 'Falta nombre_usuario'}, status=status.HTTP_400_BAD_REQUEST)
        qs = self.get_queryset().filter(nombre_usuario__iexact=nombre)
        if not qs.exists():
            return Response({'detail': 'No encontrado'}, status=status.HTTP_404_NOT_FOUND)
        usuario = qs.first()
        return Response(self.get_serializer(usuario).data)

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
    authentication_classes = [TokenAuthentication]
    service = DestinoService()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdminRole()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            destino = self.service.crear_destino(serializer.validated_data)
        except BusinessError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(destino).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            destino = self.service.actualizar_destino(instance, serializer.validated_data)
        except BusinessError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(destino).data)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            destino = self.service.actualizar_destino(instance, serializer.validated_data)
        except BusinessError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(destino).data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.service.eliminar_destino(instance)
        except BusinessError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)

class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes     = [IsAdminRole]
    service = VehiculoService()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            vehiculo = self.service.crear_vehiculo(serializer.validated_data)
        except BusinessError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(vehiculo).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            vehiculo = self.service.actualizar_vehiculo(instance, serializer.validated_data)
        except BusinessError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(vehiculo).data)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            vehiculo = self.service.actualizar_vehiculo(instance, serializer.validated_data)
        except BusinessError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(vehiculo).data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.service.eliminar_vehiculo(instance)
        except BusinessError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)

class EstadoViajeViewSet(viewsets.ModelViewSet):
    queryset = EstadoViaje.objects.all()
    serializer_class = EstadoViajeSerializer
    authentication_classes = [TokenAuthentication]
    service = EstadoViajeService()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdminRole()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            estado = self.service.crear_estado(serializer.validated_data)
        except BusinessError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(estado).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            estado = self.service.actualizar_estado(instance, serializer.validated_data)
        except BusinessError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(estado).data)


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.service.eliminar_estado(instance)
        except BusinessError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)

class PasajeroViewSet(viewsets.ModelViewSet):
    queryset = Pasajero.objects.all()
    serializer_class = PasajeroSerializer
    authentication_classes = [TokenAuthentication]
    service = PasajeroService()

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create']:  # permitir a usuarios autenticados crear pasajero
            return [IsAuthenticated()]
        return [IsAdminRole()]  # admin para update/destroy

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            pasajero = self.service.crear_pasajero(serializer.validated_data)
        except BusinessError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(pasajero).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            pasajero = self.service.actualizar_pasajero(instance, serializer.validated_data)
        except BusinessError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(pasajero).data)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            pasajero = self.service.actualizar_pasajero(instance, serializer.validated_data)
        except BusinessError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(pasajero).data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.service.eliminar_pasajero(instance)
        except BusinessError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)

class MetodoPagoViewSet(viewsets.ModelViewSet):
    queryset = MetodoPago.objects.all()
    serializer_class = MetodoPagoSerializer
    authentication_classes = [TokenAuthentication]
    service = MetodoPagoService()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]  
        return [IsAdminRole()]          


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            metodo = self.service.crear_metodo_pago(serializer.validated_data)
        except BusinessError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(metodo).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            metodo = self.service.actualizar_metodo_pago(instance, serializer.validated_data)
        except BusinessError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(metodo).data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.service.eliminar_metodo_pago(instance)
        except BusinessError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)

class EstatusPasajeViewSet(viewsets.ModelViewSet):
    queryset = EstatusPasaje.objects.all()
    serializer_class = EstatusPasajeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes     = [IsAdminRole]
    service = EstatusPasajeService()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            estatus = self.service.crear_estatus(serializer.validated_data)
        except BusinessError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(estatus).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            estatus = self.service.actualizar_estatus(instance, serializer.validated_data)
        except BusinessError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(estatus).data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.service.eliminar_estatus(instance)
        except BusinessError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ViajeViewSet(viewsets.ModelViewSet):
    queryset = ViajeService().listar_activos()
    serializer_class = ViajeSerializer
    authentication_classes = [TokenAuthentication]
    service = ViajeService()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdminRole()]

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
    authentication_classes = [TokenAuthentication]
    service = PasajeService()

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create']:
            return [IsAuthenticated()]
        return [IsAdminRole()]

    def create(self, request, *args, **kwargs):
        data = {**request.data, 'usuario_compra': request.user.id}
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            pasaje = self.service.crear_pasaje(serializer.validated_data)
        except BusinessError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(pasaje).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            pasaje = self.service.actualizar_pasaje(instance, serializer.validated_data)
        except BusinessError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(pasaje).data)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            pasaje = self.service.actualizar_pasaje(instance, serializer.validated_data)
        except BusinessError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(pasaje).data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.service.eliminar_pasaje(instance)
        except BusinessError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


class StatsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes     = [IsAuthenticated]

    def get(self, request):
        total_usuarios = Usuario.objects.filter(estado=True).count()
        total_viajes   = Viaje.objects.filter(estado=True).count()

        qs = Viaje.objects.filter(estado=True).annotate(
            mes=TruncMonth('fecha_hora_salida')
        ).values('mes').annotate(cantidad=Count('id')).order_by('mes')

        viajes_por_mes = [
            {
                'month': v['mes'].strftime('%Y-%m'),
                'count': v['cantidad']
            }
            for v in qs
        ]

        return Response({
            'total_usuarios': total_usuarios,
            'total_viajes': total_viajes,
            'viajes_por_mes': viajes_por_mes,
        })