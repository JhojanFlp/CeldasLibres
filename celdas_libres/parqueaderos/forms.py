from django import forms
from betterforms.multiform import MultiModelForm
from .models import Tarifa, EntradaVehiculo, PlanPago, DescuentoTarifa, Parqueadero, CapacidadVehiculo, SalidaVehiculo
from django.core.validators import RegexValidator
import re
from django.core.exceptions import ValidationError
from vehiculos.models import Vehiculo
from accounts.models import Usuario



def get_my_choices():
    list = Vehiculo.objects.filter()
    listV = []
    for l in list:
        listV.append((l, l))
    return listV

class CrearTarifaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CrearTarifaForm, self).__init__(*args, **kwargs)
        self.fields['tipo_vehiculo'] = forms.ChoiceField(
            choices=get_my_choices(),
            widget=forms.Select(
                attrs={'class': 'form-control'}
                )
            )
    # tipo_vehiculo = forms.ChoiceField(
    #     choices=get_my_choices(),
    #     widget=forms.Select(
    #         attrs={'class': 'form-control'}
    #     )
    # )

    class Meta:
        model = Tarifa
        fields = '__all__'
        widgets = {
            'tipo_vehiculo': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'por_hora': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'anno': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'type': 'hidden'
                }
            )
        }




class CrearVehiculoTarifaForm(forms.ModelForm):

     class Meta:
        model = Tarifa
        fields = '__all__'
        widgets = {
            'por_hora': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'anno': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'type': 'hidden'
                }
            ),
            'tipo_vehiculo': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            )
        }

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

class VehiculoYTarifa(MultiModelForm):
        form_classes = {
        'vehiculo':  CrearVehiculoForm,
        'tarifa': CrearVehiculoTarifaForm,
    }



class EntradaVehiculoForm(forms.ModelForm):
    tarifa=forms.ModelChoiceField(queryset=Tarifa.objects.all())
    placa=forms.CharField(
        max_length=6,
        min_length=6,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'autocomplete': 'off',
                   'pattern':'[A-Za-z0-9]+',
                   'title':'Solo ingrese caracteres alfanumericos'
                    }
            )
        )

    class Meta:
        model = EntradaVehiculo
        fields = '__all__'
        widgets = {
            'tarifa': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            )
        }

class SalidaVehiculoForm(forms.ModelForm):
    class Meta:
        model = SalidaVehiculo
        fields = ['documento']
        widgets = {
            'documento': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            )
        }



class CreatePlanPago(forms.ModelForm):
    class Meta:
        model = PlanPago
        exclude = ['creado', 'eliminado']
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'required': ''
                }
            ),
            'periodicidad': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'required': '',
                    'min': 0,
                    'max': 999
                }
            )
        }

class CreateDescuentoTarifa(forms.ModelForm):
    class Meta:
        model = DescuentoTarifa
        exclude = ['plan_pago']
        widgets = {
            'tarifa': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'descuento': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 0,
                    'max': 70
                }
            )
        }

class CrearParqueadero(forms.ModelForm):
    class Meta:
        model = Parqueadero
        fields = '__all__'
        widgets = {
            'nombre':forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'required': '',
                    'minlength' :5,
                    'maxlength' :25
                }
            ),
            'direccion':forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'required': '',
                    'minlength' :5,
                    'maxlength' :25
                }
            ),
            'telefono':forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'required':'',
                    'max':'9999999999'
                }
            ),
            'encargado':forms.Select(
                attrs={
                    'class':'form-control'
                }
            )
        }

class CrearCapacidadVehiculo(forms.ModelForm):
    class Meta:
        model = CapacidadVehiculo
        exclude = ['parqueadero']
        widgets = {
            'vehiculo':forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'required': ''
                }
            ),
            'capacidad':forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'required':'',
                    'min': 0,
                    'max': 9999
                }
            )
        }

class UpdateParqueaderoForm(forms.ModelForm):
    class Meta:
        model = Parqueadero
        fields = ['nombre', 'direccion', 'telefono', 'encargado']
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'direccion': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'telefono': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'encargado': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            )
        }