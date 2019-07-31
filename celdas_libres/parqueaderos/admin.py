from django.contrib import admin

from .forms import CrearTarifaForm
from .models import Tarifa, EntradaVehiculo, PlanPago, DescuentoTarifa, SalidaVehiculo


class TarifaAdmin(admin.ModelAdmin):
    model = Tarifa
    list_display = ['anno', 'tipo_vehiculo', 'por_hora']

class EntradaVehiculoAdmin(admin.ModelAdmin):
    model = EntradaVehiculo
    list_display = ['placa', 'fecha_ingreso', 'tarifa']

class PlanPagoAdmin(admin.ModelAdmin):
    model = PlanPago
    list_display = ['id', 'nombre', 'creado', 'periodicidad']

class DescuentoTarifaAdmin(admin.ModelAdmin):
    model = DescuentoTarifa
    list_display = ['plan_pago', 'tarifa', 'descuento']

class SalidaVehiculoAdmin(admin.ModelAdmin):
    model = SalidaVehiculo
    list_display = ['documento', 'tipo_vehiculo', 'entrada_vehiculo', 'fecha_salida']

admin.site.register(Tarifa, TarifaAdmin)
admin.site.register(EntradaVehiculo, EntradaVehiculoAdmin)
admin.site.register(PlanPago, PlanPagoAdmin)
admin.site.register(DescuentoTarifa, DescuentoTarifaAdmin)
admin.site.register(SalidaVehiculo, SalidaVehiculoAdmin)
