# Generated by Django 2.2.2 on 2019-07-17 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vehiculos', '0006_auto_20190709_0240'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehiculo',
            name='tarifa',
        ),
    ]