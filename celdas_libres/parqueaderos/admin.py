from django.contrib import admin

from .forms import CrearTarifaForm
from .models import Tarifa, EntradaVehiculo


class TarifaAdmin(admin.ModelAdmin):
    model = Tarifa
    list_display = ['anno', 'tipo_vehiculo', 'por_hora']

class EntradaVehiculoAdmin(admin.ModelAdmin):
    model = EntradaVehiculo
    list_display = ['placa', 'fecha_ingreso', 'tarifa']

admin.site.register(Tarifa, TarifaAdmin)
admin.site.register(EntradaVehiculo, EntradaVehiculoAdmin)
