from django.urls import path

from .views import CrearVehiculo, VerVehiculos, ModificarVehiculo, EliminarVehiculo, CrearVehiculoClienteFrecuente,VerVehiculosClientes,EliminarVehiculoCliente,ModificarVehiculoCliente

urlpatterns = [
    path('crear_vehiculo/', CrearVehiculo.as_view(), name='crear_vehiculo'),
    path('vehiculos/', VerVehiculos.as_view(), name='vehiculos'),
    path('modificar-vehiculo/<int:pk>', ModificarVehiculo.as_view(), name='modificar-vehiculo'),
    path('eliminar-vehiculo/<int:pk>', EliminarVehiculo.as_view(), name='eliminar-vehiculo'),
    path('crear-vehiculo-cliente/', CrearVehiculoClienteFrecuente.as_view(), name='crear-vehiculo-cliente'),
    path('vehiculos-clientes/',VerVehiculosClientes.as_view(),name='vehiculos-clientes'),
    path('eliminar-vehiculo-cliente/<int:pk>',EliminarVehiculoCliente.as_view(),name='eliminar-vehiculo-cliente'),
    path('modificar-vehiculo-cliente/<int:pk>', ModificarVehiculoCliente.as_view(),name='modificar-vehiculo-cliente'),
]