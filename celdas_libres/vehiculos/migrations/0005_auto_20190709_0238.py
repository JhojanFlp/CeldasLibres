# Generated by Django 2.2.2 on 2019-07-09 07:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehiculos', '0004_auto_20190709_0234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehiculo',
            name='tarifa',
            field=models.PositiveIntegerField(null=True, validators=[django.core.validators.MaxValueValidator(9999999), django.core.validators.MinValueValidator(0)]),
        ),
    ]