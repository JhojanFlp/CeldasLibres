from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import SignUpForm
from .models import CustomUser, Usuario


class CustomUserAdmin(UserAdmin):
    add_form = SignUpForm
    model = CustomUser
    list_display = ('id', 'username')
    list_display_links = ('id', 'username')


class UsuarioAdmin(admin.ModelAdmin):
    model = Usuario
    list_display = ('user', 'identificacion', 'tipo_identificacion',
            'nacionalidad', 'fecha_nacimiento', 'telefono', 'celular', 'direccion')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Usuario, UsuarioAdmin)
