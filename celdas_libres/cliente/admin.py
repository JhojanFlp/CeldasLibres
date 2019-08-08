from django.contrib import admin
from .models import ClienteFrecuente

class ClienteFrecuenteAdmin(admin.ModelAdmin):
    model = ClienteFrecuente
    list_display = ['identificacion', 'nombres', 'apellidos']

admin.site.register(ClienteFrecuente, ClienteFrecuenteAdmin)