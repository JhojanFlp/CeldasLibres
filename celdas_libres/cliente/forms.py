from django import forms
from betterforms.multiform import MultiModelForm
from parqueaderos.models import Tarifa, EntradaVehiculo, PlanPago, DescuentoTarifa, Parqueadero, CapacidadVehiculo, SalidaVehiculo, Factura
from django.core.validators import RegexValidator
import re
from django.core.exceptions import ValidationError
from vehiculos.models import Vehiculo
from accounts.models import Usuario
from parqueaderos.models import Parqueadero
from cliente.models import ClienteFrecuente
from django.contrib.auth.forms import UserCreationForm
import datetime
def get_my_choices3():
    list = PlanPago.objects.values_list('nombre',flat='true').filter(eliminado='False')
    listV = []
    for l in list:
        listV.append((l, l))
    return listV

class CrearClienteFrecuenteForm(forms.ModelForm):
    tipo_identificacion = forms.ChoiceField(
        required=True,
        choices=[
            ('TI', 'Tarjeta de identidad'),
            ('CC', 'Cédula de ciudadanía'),
            ('PS', 'Pasaporte'),
        ],
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )
    identificacion = forms.CharField(
        label='Identificacion',  max_length=20, min_length=3, required=True,
        widget=forms.NumberInput(
            attrs={'class': 'form-control'}
        )
    )

    nombres= forms.CharField(
        label='nombres', max_length=30, min_length=3, required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'autofocus': 'autofocus', 'id': '2dasd'}
        )
    )
    apellidos = forms.CharField(
        label='apellidos',  max_length=30, min_length=3, required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    celular = forms.CharField(max_length=15, min_length=3,required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                }
        ))
    email = forms.EmailField(
        label='Correo electrónico', required=False, max_length=40,min_length=3,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Correo electrónico'
                }
        )
    )
    planes_pago = forms.ChoiceField(required=True,
        choices=get_my_choices3(),
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
        )
    class Meta:
        model = ClienteFrecuente
        fields = [
            'identificacion','tipo_identificacion', 'nombres',
            'apellidos', 'celular', 'email', 'fecha_nacimiento',
            'planes_pago',]
    def __init__(self, *args, **kwargs):
    	super(CrearClienteFrecuenteForm, self).__init__(*args, **kwargs)

class UpdateClienteForm(forms.ModelForm):
    tipo_identificacion = forms.ChoiceField(
        #disabled=True,
        required=True,
        choices=[
            ('TI', 'Tarjeta de identidad'),
            ('CC', 'Cédula de ciudadanía'),
            ('PS', 'Pasaporte'),
        ],
        widget=forms.Select(
            #attrs={'class': 'form-control','readonly':'readonly'}
            attrs={'class': 'form-control'}
        )
    )
    identificacion = forms.CharField(
        label='Identificacion',  max_length=20, min_length=3, required=True, disabled=True,
        widget=forms.NumberInput(
            attrs={'class': 'form-control','readonly':'readonly'}
        )
    )

    nombres= forms.CharField(
        label='nombres', max_length=30, min_length=3, required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'autofocus': 'autofocus', 'id': '2dasd'}
        )
    )
    apellidos = forms.CharField(
        label='apellidos',  max_length=30, min_length=3, required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    celular = forms.CharField(max_length=15, min_length=3,required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                }
        ))
    email = forms.EmailField(
        label='Correo electrónico', required=False, max_length=40,min_length=3,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Correo electrónico'
                }
        )
    )
    planes_pago = forms.ChoiceField(required=True,
        choices=get_my_choices3(),
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
        )
    class Meta:
        model = ClienteFrecuente
        fields = [
            'identificacion','tipo_identificacion', 'nombres',
            'apellidos', 'celular', 'email', 'fecha_nacimiento',
            'planes_pago',]
    def __init__(self, *args, **kwargs):
    	super(UpdateClienteForm, self).__init__(*args, **kwargs)
