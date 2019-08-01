from datetime import datetime

from django.core.validators import (MaxLengthValidator, MaxValueValidator,
                                    MinLengthValidator, MinValueValidator)
from django.db import models

from accounts.models import Usuario
from vehiculos.models import Vehiculo

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
        ordering = ['-creado']
        verbose_name = 'plan de pago'

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


class Parqueadero(models.Model):
    nombre = models.CharField(unique=True, primary_key=True,validators=[MinLengthValidator(5), MaxLengthValidator(25)],max_length=25)
    direccion = models.CharField(validators=[MinLengthValidator(5), MaxLengthValidator(25)],max_length=25)
    telefono = models.PositiveIntegerField(validators=[MaxValueValidator(9999999999)])
    encargado = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.nombre).capitalize()

class CapacidadVehiculo(models.Model):
    parqueadero = models.ForeignKey(Parqueadero, on_delete=models.CASCADE, related_name="capacidades")
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    capacidad = models.PositiveIntegerField(validators=[MaxValueValidator(9999)])

    def __str__(self):
        return str(self.vehiculo+" "+self.capacidad).capitalize()

class EntradaVehiculo(models.Model):
    tarifa = models.ForeignKey(Tarifa, on_delete=models.SET_NULL, null=True, related_name='tarifa')
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    placa = models.CharField(max_length=6)
    usuario=models.CharField(max_length=20,null=True)
    parqueadero = models.ForeignKey(Parqueadero, on_delete=models.CASCADE,null=True, related_name='parq')

    class Meta:
        unique_together = (('placa', 'fecha_ingreso'),)
        verbose_name =  'entrada vehiculo'
        ordering = ['fecha_ingreso']

    def __str__(self):
        return str(self.placa)

class SalidaVehiculo(models.Model):
    documento = models.CharField(max_length=20)
    tipo_vehiculo =  models.CharField(max_length=10)
    fecha_salida = models.DateTimeField(auto_now_add=True)
    entrada_vehiculo = models.ForeignKey(
        EntradaVehiculo, on_delete=models.SET_NULL, null=True
    )
    operario = models.ForeignKey(
        Usuario, on_delete=models.SET_NULL, null=True
    )

class Factura(models.Model):
    serial = models.CharField(unique=True, primary_key=True,validators=[MinLengthValidator(5), MaxLengthValidator(25)],max_length=25)
    name = models.CharField(validators=[MinLengthValidator(5), MaxLengthValidator(25)],max_length=25)
    phone = models.PositiveIntegerField(validators=[MaxValueValidator(9999999999)])
    ubication = models.CharField(validators=[MinLengthValidator(5), MaxLengthValidator(25)],max_length=25)
    id_user = models.CharField(max_length=20,null=False)
    placa = models.CharField(max_length=6,null=False)
    in_date = models.DateTimeField(auto_now_add=False)
    out_date = models.DateTimeField(auto_now_add=True)
    total = models.PositiveIntegerField(validators=[MaxValueValidator(9999999999)])

    def __str__(self):
        return str(self.name)