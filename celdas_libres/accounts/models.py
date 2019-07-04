from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models


def default_id():
    return Usuario.objects.count()


class CustomUser(AbstractUser):
    def __str__(self):
        return self.username

class Usuario(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='usuario', primary_key=True, default=0
    )
    identificacion = models.CharField(max_length=15)
    tipo_identificacion = models.CharField(max_length=15, null=True)
    nacionalidad = models.CharField(max_length=20, null=True)
    fecha_nacimiento = models.DateField(null=True)
    telefono = models.BigIntegerField(null=True)
    celular = models.BigIntegerField(null=True)
    direccion = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, *args, **kwargs):
    if created:
        Usuario.objects.get_or_create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, *args, **kwargs):
    instance.usuario.identificacion = instance.username
    instance.usuario.save()