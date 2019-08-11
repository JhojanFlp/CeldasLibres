from datetime import datetime
from django.db import models
from parqueaderos.models import PlanPago
from accounts.models import Usuario
from vehiculos.models import Vehiculo


class ClienteFrecuente(models.Model):
    identificacion=models.BigIntegerField(primary_key=True)
    tipo_documento=models.CharField(max_length=20)
    nombres=models.CharField(max_length=30)
    apellidos=models.CharField(max_length=30)
    numero_celular=models.BigIntegerField()
    email=models.EmailField(max_length=40,null=True)
    fecha_nacimiento=models.DateTimeField()
    plan_pago=models.ForeignKey(
        PlanPago, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        respuesta = str(self.identificacion) + " - "+str(self.nombres)+" "+str(self.apellidos)
        return respuesta
