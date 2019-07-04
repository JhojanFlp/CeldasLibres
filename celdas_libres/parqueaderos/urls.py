from django.urls import path

from .views import CrearTarifa, VerTarifas, CrearEntradaVehiculo, VerIngresados, ModificarTarifa, EliminarTarifa

urlpatterns = [
    path('crear_tarifa/', CrearTarifa.as_view(), name='crear_tarifa'),
    path('tarifas/', VerTarifas.as_view(), name='tarifas'),
    path('ingresar-vehiculo/', CrearEntradaVehiculo.as_view(), name='ingresar-vehiculo'),
    path('vehiculos-ingresados/', VerIngresados.as_view(), name='vehiculos-ingresados'),
    path('modificar-tarifa/<int:pk>', ModificarTarifa.as_view(), name='modificar-tarifa'),
    path('eliminar-tarifa/<int:pk>', EliminarTarifa.as_view(), name='eliminar-tarifa'),
]
