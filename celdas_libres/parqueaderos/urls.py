from django.urls import path

from .views import (CrearEntradaVehiculo, CrearPlanPago, CrearTarifa,
                    EliminarTarifa, ModificarTarifa, VerIngresados, VerTarifas,
                    VerPlanesPago, ModificarPlanPago, EliminarPlanPago)

urlpatterns = [
    path('crear-tarifa/', CrearTarifa.as_view(), name='crear-tarifa'),
    path('tarifas/', VerTarifas.as_view(), name='tarifas'),
    path('ingresar-vehiculo/', CrearEntradaVehiculo.as_view(), name='ingresar-vehiculo'),
    path('vehiculos-ingresados/', VerIngresados.as_view(), name='vehiculos-ingresados'),
    path('modificar-tarifa/<int:pk>', ModificarTarifa.as_view(), name='modificar-tarifa'),
    path('eliminar-tarifa/<int:pk>', EliminarTarifa.as_view(), name='eliminar-tarifa'),
    path('crear-plan-pago/', CrearPlanPago.as_view(), name='crear-plan-pago'),
    path('planes-pago/', VerPlanesPago.as_view(), name='planes-pago'),
    path('modificar-plan-pago/<int:pk>', ModificarPlanPago.as_view(), name='modificar-plan-pago'),
    path('eliminar-plan-pago/<int:pk>', EliminarPlanPago.as_view(), name='eliminar-plan-pago'),
]
