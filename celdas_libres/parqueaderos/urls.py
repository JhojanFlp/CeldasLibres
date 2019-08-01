from django.urls import path


from .views import (CrearEntradaVehiculo, CrearPlanPago, CrearTarifa,
                    EliminarTarifa, ModificarTarifa, VerIngresados, VerTarifas,
                    VerPlanesPago, ModificarPlanPago, EliminarPlanPago,
                    ModificarParqueadero, CrearParqueadero, VerParqueaderos,
                    EliminarParqueadero, VerPlanesPago, ModificarPlanPago, EliminarPlanPago,VerFicho)
from vehiculos.views import CrearVehiculo

from .views import (CrearEntradaVehiculo, CrearParqueadero, CrearPlanPago,
                    CrearSalidaVehiculo, CrearTarifa, EliminarParqueadero, EliminarPlanPago, EliminarTarifa,
                    ModificarParqueadero, ModificarPlanPago, ModificarTarifa,
                    VerFicho, VerIngresados, VerParqueaderos, VerPlanesPago,
                    VerTarifas,GenerarBalance)


urlpatterns = [
    path('crear-tarifa/', CrearTarifa.as_view(), name='crear-tarifa'),
    path('tarifas/', VerTarifas.as_view(), name='tarifas'),
    path('entrada-vehiculo/', CrearEntradaVehiculo.as_view(), name='ingresar-vehiculo'),
    path('salida-vehiculo/<int:pk>', CrearSalidaVehiculo.as_view(), name='salida-vehiculo'),
    path('vehiculos-ingresados/', VerIngresados.as_view(), name='vehiculos-ingresados'),
    path('modificar-tarifa/<int:pk>', ModificarTarifa.as_view(), name='modificar-tarifa'),
    path('eliminar-tarifa/<int:pk>', EliminarTarifa.as_view(), name='eliminar-tarifa'),
    path('crear-plan-pago/', CrearPlanPago.as_view(), name='crear-plan-pago'),
    path('planes-pago/', VerPlanesPago.as_view(), name='planes-pago'),
    path('modificar-plan-pago/<int:pk>', ModificarPlanPago.as_view(), name='modificar-plan-pago'),
    path('eliminar-plan-pago/<int:pk>', EliminarPlanPago.as_view(), name='eliminar-plan-pago'),
    path('crear-parqueadero/',CrearParqueadero.as_view(), name='crear-parqueadero'),
    path('parqueaderos/', VerParqueaderos.as_view(), name='parqueaderos'),
    path('modificar-parqueadero/<str:pk>', ModificarParqueadero.as_view(), name='modificar-parqueadero'),
    path('eliminar-parqueadero/<str:pk>', EliminarParqueadero.as_view(), name='eliminar-parqueadero'),
    path('ver-ficho/<int:pk>', VerFicho.as_view(), name='ficho-parqueadero'),
    path('balance/',GenerarBalance.as_view(),name='Generar_Balance')
]
