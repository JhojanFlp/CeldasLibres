# Generated by Django 2.2.2 on 2019-07-24 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parqueaderos', '0010_auto_20190724_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entradavehiculo',
            name='nombre_parq',
            field=models.CharField(default='Estacionamiento Ayacucho', max_length=50),
        ),
    ]
