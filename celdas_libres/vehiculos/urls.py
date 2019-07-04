from django.urls import path

from .views import CrearVehiculo, VerVehiculos, ModificarVehiculo, EliminarVehiculo

urlpatterns = [
    path('crear_vehiculo/', CrearVehiculo.as_view(), name='crear_vehiculo'),
    path('vehiculos/', VerVehiculos.as_view(), name='vehiculos'),
    path('modificar-vehiculo/<int:pk>', ModificarVehiculo.as_view(), name='modificar-vehiculo'),
    path('eliminar-vehiculo/<int:pk>', EliminarVehiculo.as_view(), name='eliminar-vehiculo'),
]