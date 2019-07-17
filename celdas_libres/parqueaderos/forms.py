from django import forms
from .models import Tarifa, EntradaVehiculo, PlanPago, DescuentoTarifa
from django.core.validators import RegexValidator
import re
from django.core.exceptions import ValidationError
from vehiculos.models import Vehiculo



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