from django.db import models
from datetime import datetime
from django.core.validators import MaxValueValidator

# Create your models here.

def current_year():
    return datetime.now().year

class Vehiculo(models.Model):
    tipo_vehiculo = models.CharField(max_length=20, unique=True)
    # tarifa = models.PositiveIntegerField(null=True,validators=[
    #         MaxValueValidator(9999999)
    #     ])
    anno = models.PositiveIntegerField(default=current_year, verbose_name="año")

    def __str__(self):
        return str(self.tipo_vehiculo).capitalize()

class VehiculoClienteFrecuente(models.Model):
    placa = models.CharField(max_length=6)
    color = models.CharField(max_length=20)
    tipo_vehiculo = models.CharField(max_length=20)
    propietario = models.BigIntegerField()

    class Meta:
        verbose_name = 'vehiculos_clientes'

    def __str__(self):
        return str(self.placa)+" "+str(self.color)