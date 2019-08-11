from django import forms
from bootstrap_modal_forms.forms import BSModalForm
from .models import Vehiculo, VehiculoClienteFrecuente
#from parqueaderos.models import Tarifa
from cliente.models import ClienteFrecuente

def get_vehiculos_choices():
    list = Vehiculo.objects.filter()
    listV = []
    for l in list:
        listV.append((l, l))
    return listV

def get_cliente_choices():
    list = ClienteFrecuente.objects.filter()
    listV = []
    for l in list:
        listV.append((l.identificacion,str(l)))
    return listV

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
            'anno': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'type': 'hidden'

                }
            )
        }

class CrearVehiculoClienteFrecuenteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CrearVehiculoClienteFrecuenteForm, self).__init__(*args, **kwargs)
        self.fields['tipo_vehiculo'] = forms.ChoiceField(
            choices=get_vehiculos_choices(),
            widget=forms.Select(
                attrs={'class': 'form-control'}
                )
            )
        self.fields['propietario']= forms.ChoiceField(
            choices=get_cliente_choices(),
            widget=forms.Select(
                attrs={'class': 'form-control'}
                )
            )

    class Meta:
        model = VehiculoClienteFrecuente
        fields = '__all__'
        widgets = {
            'placa' : forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'required': '',
                    'maxlength' :6
                }
            ),
            'color' : forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'required': '',
                    'minlength' :3,
                    'maxlength' :20
                }
            ),
            'tipo_vehiculo' : forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': '',
                }
            ),
            'propietario' : forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': '',
                }
            )
        }