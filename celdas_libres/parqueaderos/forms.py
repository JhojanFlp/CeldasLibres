from django import forms
from .models import Tarifa, EntradaVehiculo


class CrearTarifaForm(forms.ModelForm):
    tipo_vehiculo = forms.ChoiceField(
        choices=[
            ('carro', 'Carro'),
            ('moto', 'Moto'),
        ],
    )

    class Meta:
        model = Tarifa
        fields = '__all__'
        widgets = {
            'anno': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'readonly': True
                }
            ),
            'tipo_vehiculo': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'por_hora': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            )
        }


class EntradaVehiculoForm(forms.ModelForm):
    tarifa=forms.ModelChoiceField(queryset=Tarifa.objects.all())
    placa=forms.CharField(max_length=6)
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
