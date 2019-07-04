from datetime import datetime
from django.db import models

def default_id():
    return datetime.now().year

class Tarifa(models.Model):
    anno = models.PositiveIntegerField(default=default_id, verbose_name="año")
    tipo_vehiculo = models.CharField(max_length=10)
    por_hora = models.PositiveIntegerField()

    class Meta:
        unique_together = (('anno', 'tipo_vehiculo'),)
        verbose_name =  'tarifa'
        ordering = ['anno']

    def __str__(self):
        #+ ' ' + str(self.anno) + ' por ' + str(self.por_hora) + ' h'
        return str(self.tipo_vehiculo).capitalize()

class EntradaVehiculo(models.Model):
    tarifa = models.ForeignKey(Tarifa, on_delete=models.SET_NULL, null=True)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    placa = models.CharField(max_length=6)

    class Meta:
        unique_together = (('placa', 'fecha_ingreso'),)
        verbose_name =  'entrada vehiculo'
        ordering = ['fecha_ingreso']

    def __str__(self):
        return str(self.placa)