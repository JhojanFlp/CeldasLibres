# Generated by Django 2.2.2 on 2019-07-22 15:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parqueaderos', '0007_capacidadvehiculo_parqueadero'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parqueadero',
            name='eliminado',
        ),
    ]
