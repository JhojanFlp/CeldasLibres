# Generated by Django 2.2.2 on 2019-07-24 22:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parqueaderos', '0015_remove_entradavehiculo_nom_parq'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entradavehiculo',
            name='dir_parq',
        ),
    ]
