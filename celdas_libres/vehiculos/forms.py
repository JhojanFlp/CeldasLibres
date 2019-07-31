from django import forms
from bootstrap_modal_forms.forms import BSModalForm
from .models import Vehiculo
#from parqueaderos.models import Tarifa

class CrearVehiculoForm(BSModalForm):


    class Meta:
        model = Vehiculo
        fields = '__all__'
        widgets = {
            'tipo_vehiculo' : forms.TextInput(
                attrs={
                    'class':'form-control'
                }
            ),
            # 'tarifa': forms.NumberInput(
            #     attrs={
            #         'class': 'form-control'
            #     }
            # ),
            'anno': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'type': 'hidden'

                }
            )
        }