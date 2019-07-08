from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Usuario

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        label='Primer nombre', max_length=40, min_length=2, required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'autofocus': 'autofocus', 'id': '2dasd'}
        )
    )
    last_name = forms.CharField(
        label='Primer apellidos',  max_length=40, min_length=2, required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    # Username es con lo que se va a logear, que en este caso lo vamos a tratar como la identificacion
    username = forms.CharField(
        label='Identificacion',  max_length=15, min_length=5, required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    password1 = forms.CharField(
        label='Contraseña', required=True, max_length=40, min_length=6,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )
    password2 = forms.CharField(
        label='Verificar contraseña', required=True, max_length=40, min_length=6,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )
    email = forms.EmailField(
        label='Correo electrónico', required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Correo electrónico'
                }
        )
    )
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
    nacionalidad = forms.ChoiceField(required=True,
        choices=[
            ('COL', 'Colombiana'),
            ('VEN', 'Venezolana'),
            ('ECU', 'Ecuatoriana'),
            ('ESP', 'Española'),
            ('CHI', 'Chilena'),
            ('PER', 'Peruana'),
            ('PAN', 'Panameña'),
        ],
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
        )
    fecha_nacimiento = forms.DateField(input_formats=['%d/%m/%Y'],
    required=True,
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )
    telefono = forms.CharField(max_length=15, required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                }
        ))
    celular = forms.CharField(max_length=15, required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                }
        ))
    direccion = forms.CharField(max_length=30, required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                }
        ))

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'username',
            'password1', 'password2', 'email', 'tipo_identificacion',
            'nacionalidad', 'fecha_nacimiento', 'telefono', 'celular',
            'direccion',
            ]

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Identificacion', required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'autofocus': 'autofocus'
                }
        )
    )
    password = forms.CharField(
        label='Contraseña', required=True,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Contraseña'}
        )
    )

class UpdateUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nacionalidad', 'fecha_nacimiento',
                  'telefono', 'celular', 'direccion']
        widgets = {
            'nacionalidad': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    }
            ),
            'fecha_nacimiento': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'dd/mm/aaaa'
                    }
            ),
            'telefono': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    }
            ),
            'celular': forms.TextInput(
                    attrs={
                        'class': 'form-control',
                        }
                ),
            'direccion': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    }
            )
        }
