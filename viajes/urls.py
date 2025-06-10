from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from .views import (
    RolViewSet, TipoTransporteViewSet, UsuarioViewSet, DestinoViewSet,
    VehiculoViewSet, EstadoViajeViewSet, PasajeroViewSet, MetodoPagoViewSet,
    EstatusPasajeViewSet, ViajeViewSet, PasajeViewSet
)
from .views import LoginView

router = DefaultRouter()
router.register(r'roles', RolViewSet, basename='rol')
router.register(r'tipos-transporte', TipoTransporteViewSet, basename='tipotransporte')
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'destinos', DestinoViewSet, basename='destino')
router.register(r'vehiculos', VehiculoViewSet, basename='vehiculo')
router.register(r'estados-viaje', EstadoViajeViewSet, basename='estadoviaje')
router.register(r'pasajeros', PasajeroViewSet)
router.register(r'metodos-pago', MetodoPagoViewSet)
router.register(r'estatus-pasaje', EstatusPasajeViewSet)
router.register(r'viajes', ViajeViewSet, basename='viaje')
router.register(r'pasajes', PasajeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
]
