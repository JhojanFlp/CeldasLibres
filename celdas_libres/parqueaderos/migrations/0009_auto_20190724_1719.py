# Generated by Django 2.2.2 on 2019-07-24 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parqueaderos', '0008_auto_20190724_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='entradavehiculo',
            name='direccion_parq',
            field=models.CharField(default='Cl 49 55-77', max_length=30),
        ),
        migrations.AddField(
            model_name='entradavehiculo',
            name='nombre_parq',
            field=models.CharField(default='Estacionamiento Ayacucho', max_length=50),
        ),
        migrations.AddField(
            model_name='entradavehiculo',
            name='telefono_parq',
            field=models.PositiveIntegerField(default=573820, max_length=10),
        ),
    ]
