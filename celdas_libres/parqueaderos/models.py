from datetime import datetime

from django.core.validators import (MaxLengthValidator, MaxValueValidator,
                                    MinLengthValidator, MinValueValidator)
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

class PlanPago(models.Model):
    nombre = models.CharField(
        validators=[MinLengthValidator(5), MaxLengthValidator(15)],
        max_length=15
    )
    creado = models.DateField(auto_now_add=True)
    periodicidad = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(999)]
    )
    eliminado = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'plan de pago'
        ordering = ['nombre']

    def __str__(self):
        return str(self.nombre).capitalize()

class DescuentoTarifa(models.Model):
    plan_pago = models.ForeignKey(
        PlanPago, on_delete=models.CASCADE, related_name='descuentos'
    )
    tarifa = models.ForeignKey(Tarifa, on_delete=models.CASCADE)
    descuento = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(70.0)],
        default=0.0
    )

    class Meta:
        verbose_name =  'descuento tarifa'
        ordering = ['descuento']

    def __str__(self):
        return str(self.tarifa).capitalize() + ' ' + str(self.descuento) + '%'

    @property
    def get_descuento(self):
        return str(self.descuento).replace(',', '.')