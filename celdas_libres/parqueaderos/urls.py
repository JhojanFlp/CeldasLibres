from django.urls import path


from .views import (CrearEntradaVehiculo, CrearPlanPago, CrearTarifa,
                    EliminarTarifa, ModificarTarifa, VerIngresados, VerTarifas,
                    VerPlanesPago, ModificarPlanPago, EliminarPlanPago,
                    ModificarParqueadero, CrearParqueadero, VerParqueaderos,
                    EliminarParqueadero, VerPlanesPago, ModificarPlanPago, EliminarPlanPago,VerFicho)
from vehiculos.views import CrearVehiculo
from cliente.views import CrearClienteFrecuente,VerClientesFrecuentes,EliminarCliente, ModificarCliente
from .views import (CrearEntradaVehiculo, CrearParqueadero, CrearPlanPago,
                    CrearSalidaVehiculo, CrearTarifa, EliminarParqueadero, EliminarPlanPago, EliminarTarifa,
                    ModificarParqueadero, ModificarPlanPago, ModificarTarifa,
                    VerFicho, VerIngresados, VerParqueaderos, VerPlanesPago,
                    VerTarifas, GenerarFactura, VerBalance, GenerarBalance, HistorialSalidas, HistorialFacturas, buscar_cliente)


urlpatterns = [
    path('crear-tarifa/', CrearTarifa.as_view(), name='crear-tarifa'),
    path('historial-salidas/', HistorialSalidas.as_view(), name='historial-salidas'),
    path('historial-facturas/', HistorialFacturas.as_view(), name='historial-facturas'),
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

    path('generar-factura/', GenerarFactura.as_view(), name='generar-factura'),


    path('ver-balance/(?P<parqueadero>[0-9]+/$)/(?P<desde>[0-9]+/$)/(?P<hasta>[0-9]+/$)/', VerBalance.as_view(), name='ver-balance'),

    path('balance/',GenerarBalance.as_view(),name='Generar_Balance'),

    #path('ver-balance/', VerBalance.as_view(), name='ver-balance'),

    path('balance/',GenerarBalance.as_view(),name='Generar_Balance'),
    path('crear-cliente-frecuente/',CrearClienteFrecuente.as_view(),name='crear-cliente-frecuente'),
    path('ver-cliente-frecuente/',VerClientesFrecuentes.as_view(),name='ver-cliente-frecuente'),
    path('modificar-cliente/', GenerarFactura.as_view(), name='generar-factura'),

    path('buscar-cliente/<str:identificacion>/', buscar_cliente, name='buscar-cliente'),
    path('eliminar-clientefrecuente/<int:pk>', EliminarCliente.as_view(), name='eliminar-clientefrecuente'),
    path('modificar-cliente/<int:pk>',ModificarCliente.as_view(),name='modificar_cliente')
]
