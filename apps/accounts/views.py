"""
Archivo: views.py
Aplicación: accounts
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripción: Define las vistas para registro, inicio y cierre de sesión.
"""

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import redirect, render

from .forms import LoginForm, RegistroClienteForm
from .models import Cliente, PerfilUsuario


def register_client(request):
    """
    Permite registrar un nuevo cliente y crear su usuario de acceso.
    """

    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            with transaction.atomic():
                user = User.objects.create_user(
                    username=data['email'],
                    email=data['email'],
                    password=data['password1'],
                    first_name=data['nombres'],
                    last_name=data['apellidos']
                )

                PerfilUsuario.objects.create(
                    user=user,
                    rol=PerfilUsuario.ROL_CLIENTE,
                    telefono=data['telefono'],
                    activo=True
                )

                Cliente.objects.create(
                    user=user,
                    dni=data['dni'],
                    nombres=data['nombres'],
                    apellidos=data['apellidos'],
                    email=data['email'],
                    telefono=data['telefono'],
                    direccion=data['direccion'],
                    distrito=data['distrito'],
                    activo=True
                )

            messages.success(request, 'Cuenta creada correctamente. Ahora puedes iniciar sesión.')
            return redirect('accounts:login')

    else:
        form = RegistroClienteForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """
    Permite iniciar sesión usando correo y contraseña.
    """

    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email'].lower()
            password = form.cleaned_data['password']

            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenido, {user.first_name or user.username}.')
                return redirect('core:home')

            messages.error(request, 'Correo o contraseña incorrectos.')

    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """
    Cierra la sesión activa del usuario.
    """

    logout(request)
    messages.success(request, 'Sesión cerrada correctamente.')
    return redirect('core:home')