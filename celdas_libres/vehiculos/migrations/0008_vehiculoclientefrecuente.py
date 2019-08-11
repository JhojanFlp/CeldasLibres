# Generated by Django 2.1.1 on 2019-08-11 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehiculos', '0007_remove_vehiculo_tarifa'),
    ]

    operations = [
        migrations.CreateModel(
            name='VehiculoClienteFrecuente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placa', models.CharField(max_length=6)),
                ('color', models.CharField(max_length=20)),
                ('tipo_vehiculo', models.CharField(max_length=20)),
                ('propietario', models.BigIntegerField()),
            ],
        ),
    ]
