# Generated by Django 2.2.2 on 2019-08-14 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parqueaderos', '0030_entradavehiculo_estado_facturado'),
    ]

    operations = [
        migrations.AddField(
            model_name='planpago',
            name='identificacion',
            field=models.CharField(default='Null', max_length=20),
            preserve_default=False,
        ),
    ]
