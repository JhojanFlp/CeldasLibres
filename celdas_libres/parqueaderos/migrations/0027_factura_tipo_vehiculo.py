# Generated by Django 2.1.1 on 2019-08-01 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parqueaderos', '0026_auto_20190731_2200'),
    ]

    operations = [
        migrations.AddField(
            model_name='factura',
            name='tipo_vehiculo',
            field=models.CharField(default='no tiene', max_length=20),
            preserve_default=False,
        ),
    ]
