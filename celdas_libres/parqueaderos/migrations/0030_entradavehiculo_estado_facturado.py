# Generated by Django 2.2.2 on 2019-08-02 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parqueaderos', '0029_auto_20190802_0947'),
    ]

    operations = [
        migrations.AddField(
            model_name='entradavehiculo',
            name='estado_facturado',
            field=models.BooleanField(default=False),
        ),
    ]
