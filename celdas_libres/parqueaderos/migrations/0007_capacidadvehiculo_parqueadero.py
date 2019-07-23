# Generated by Django 2.2.2 on 2019-07-22 14:52

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vehiculos', '0007_remove_vehiculo_tarifa'),
        ('accounts', '0008_auto_20190703_1725'),
        ('parqueaderos', '0006_auto_20190717_1417'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parqueadero',
            fields=[
                ('nombre', models.CharField(max_length=25, primary_key=True, serialize=False, unique=True, validators=[django.core.validators.MinLengthValidator(5), django.core.validators.MaxLengthValidator(25)])),
                ('direccion', models.CharField(max_length=25, validators=[django.core.validators.MinLengthValidator(5), django.core.validators.MaxLengthValidator(25)])),
                ('telefono', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(9999999999)])),
                ('eliminado', models.BooleanField(default=False)),
                ('encargado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Usuario')),
            ],
        ),
        migrations.CreateModel(
            name='CapacidadVehiculo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capacidad', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(9999)])),
                ('parqueadero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='capacidades', to='parqueaderos.Parqueadero')),
                ('vehiculo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vehiculos.Vehiculo')),
            ],
        ),
    ]