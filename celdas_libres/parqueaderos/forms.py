from django import forms
from .models import Tarifa, EntradaVehiculo


class CrearTarifaForm(forms.ModelForm):
    #AQUÍ SE DEBEN PONER LOS TIPOS DE VEHÍCULOS, NO ESAS OPCIONES
    tipo_vehiculo = forms.ChoiceField(
        choices=[
            ('carro', 'Carro'),
            ('moto', 'Moto'),
        ],
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )

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
    placa=forms.CharField( max_length=15, min_length=5, required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
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
