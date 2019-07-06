from django import forms

from .models import Vehiculo
from parqueaderos.models import Tarifa

class CrearVehiculoForm(forms.ModelForm):


    class Meta:
        model = Vehiculo
        fields = '__all__'
        widgets = {
            'tipo_vehiculo' : forms.TextInput(
                attrs={
                    'class':'form-control'
                }
            ),
            'tarifa': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'anno': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'readonly': True
                }
            )
        }