"""
Archivo: forms.py
Aplicación: accounts
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripción: Define los formularios para registro, inicio de sesión y edición de perfil.
"""

from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from .models import Cliente


class RegistroClienteForm(forms.Form):
    """
    Formulario para registrar nuevos clientes en el sistema.
    """

    dni_validator = RegexValidator(
        regex=r'^\d{8}$',
        message='El DNI debe contener exactamente 8 dígitos.'
    )

    telefono_validator = RegexValidator(
        regex=r'^\d{9}$',
        message='El teléfono debe contener exactamente 9 dígitos.'
    )

    nombres = forms.CharField(max_length=100)
    apellidos = forms.CharField(max_length=100)
    dni = forms.CharField(max_length=8, validators=[dni_validator])
    telefono = forms.CharField(max_length=9, validators=[telefono_validator])
    email = forms.EmailField()
    direccion = forms.CharField(max_length=200)
    distrito = forms.CharField(max_length=100)

    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput
    )

    def clean_dni(self):
        dni = self.cleaned_data['dni']

        if Cliente.objects.filter(dni=dni).exists():
            raise forms.ValidationError('Ya existe un cliente registrado con este DNI.')

        return dni

    def clean_email(self):
        email = self.cleaned_data['email'].lower()

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Ya existe un usuario registrado con este correo.')

        if Cliente.objects.filter(email=email).exists():
            raise forms.ValidationError('Ya existe un cliente registrado con este correo.')

        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')

        if password1 and len(password1) < 8:
            raise forms.ValidationError('La contraseña debe tener como mínimo 8 caracteres.')

        return cleaned_data


class LoginForm(forms.Form):
    """
    Formulario para iniciar sesión con correo y contraseña.
    """

    email = forms.EmailField()
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput
    )


class EditarPerfilClienteForm(forms.Form):
    """
    Formulario para editar datos básicos del cliente.
    """

    telefono_validator = RegexValidator(
        regex=r'^\d{9}$',
        message='El teléfono debe contener exactamente 9 dígitos.'
    )

    nombres = forms.CharField(max_length=100)
    apellidos = forms.CharField(max_length=100)
    email = forms.EmailField()
    telefono = forms.CharField(max_length=9, validators=[telefono_validator])
    direccion = forms.CharField(max_length=200)
    distrito = forms.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.cliente = kwargs.pop('cliente', None)
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email'].lower()

        if self.user:
            if User.objects.filter(email=email).exclude(pk=self.user.pk).exists():
                raise forms.ValidationError('Este correo ya está registrado por otro usuario.')

            if User.objects.filter(username=email).exclude(pk=self.user.pk).exists():
                raise forms.ValidationError('Este correo ya está siendo usado como usuario.')

        if self.cliente:
            if Cliente.objects.filter(email=email).exclude(pk=self.cliente.pk).exists():
                raise forms.ValidationError('Este correo ya está registrado por otro cliente.')

        return email