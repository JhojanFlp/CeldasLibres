# Generated by Django 2.2.2 on 2019-07-17 17:09

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parqueaderos', '0004_auto_20190702_2038'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlanPago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=15, validators=[django.core.validators.MinLengthValidator(5), django.core.validators.MaxLengthValidator(15)])),
                ('creado', models.DateField(auto_now_add=True)),
                ('periodicidad', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(999)])),
                ('eliminado', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'plan de pago',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='DescuentoTarifa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descuento', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(70.0)])),
                ('plan_pago', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parqueaderos.PlanPago')),
                ('tarifa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parqueaderos.Tarifa')),
            ],
            options={
                'verbose_name': 'descuento tarifa',
                'ordering': ['descuento'],
            },
        ),
    ]