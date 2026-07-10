"""
Archivo: views.py
Aplicación: accounts
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripción: Define las vistas para registro, login, logout, perfil y pedidos del cliente.
"""

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from apps.delivery.models import Entrega
from apps.orders.models import Pedido
from apps.payments.models import Comprobante, Venta

from .forms import EditarPerfilClienteForm, LoginForm, RegistroClienteForm
from .models import Cliente, PerfilUsuario


def obtener_cliente_actual(user):
    """
    Obtiene el cliente asociado al usuario autenticado.
    """
    try:
        return user.cliente
    except Cliente.DoesNotExist:
        return None


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

            if user is None:
                try:
                    usuario_encontrado = User.objects.get(email=email)
                    user = authenticate(
                        request,
                        username=usuario_encontrado.username,
                        password=password
                    )
                except User.DoesNotExist:
                    user = None

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


@login_required
def profile(request):
    """
    Muestra el perfil del cliente autenticado.
    """

    cliente = obtener_cliente_actual(request.user)

    if not cliente:
        messages.error(request, 'Tu usuario no tiene un perfil de cliente asociado.')
        return redirect('core:home')

    pedidos_recientes = Pedido.objects.filter(
        cliente=cliente
    ).order_by('-fecha_pedido')[:5]

    total_pedidos = Pedido.objects.filter(cliente=cliente).count()

    pedidos_entregados = Pedido.objects.filter(
        cliente=cliente,
        estado=Pedido.ESTADO_ENTREGADO
    ).count()

    pedidos_pendientes = Pedido.objects.filter(
        cliente=cliente
    ).exclude(
        estado__in=[Pedido.ESTADO_ENTREGADO, Pedido.ESTADO_CANCELADO]
    ).count()

    context = {
        'cliente': cliente,
        'pedidos_recientes': pedidos_recientes,
        'total_pedidos': total_pedidos,
        'pedidos_entregados': pedidos_entregados,
        'pedidos_pendientes': pedidos_pendientes,
    }

    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile(request):
    """
    Permite editar los datos básicos del perfil del cliente.
    """

    cliente = obtener_cliente_actual(request.user)

    if not cliente:
        messages.error(request, 'Tu usuario no tiene un perfil de cliente asociado.')
        return redirect('core:home')

    if request.method == 'POST':
        form = EditarPerfilClienteForm(
            request.POST,
            user=request.user,
            cliente=cliente
        )

        if form.is_valid():
            data = form.cleaned_data

            with transaction.atomic():
                request.user.first_name = data['nombres']
                request.user.last_name = data['apellidos']
                request.user.email = data['email']
                request.user.username = data['email']
                request.user.save()

                cliente.nombres = data['nombres']
                cliente.apellidos = data['apellidos']
                cliente.email = data['email']
                cliente.telefono = data['telefono']
                cliente.direccion = data['direccion']
                cliente.distrito = data['distrito']
                cliente.save()

                if hasattr(request.user, 'perfil'):
                    request.user.perfil.telefono = data['telefono']
                    request.user.perfil.save()

            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('accounts:profile')

    else:
        form = EditarPerfilClienteForm(
            initial={
                'nombres': cliente.nombres,
                'apellidos': cliente.apellidos,
                'email': cliente.email,
                'telefono': cliente.telefono,
                'direccion': cliente.direccion,
                'distrito': cliente.distrito,
            },
            user=request.user,
            cliente=cliente
        )

    return render(request, 'accounts/edit_profile.html', {
        'form': form,
        'cliente': cliente,
    })


@login_required
def my_orders(request):
    """
    Muestra el historial de pedidos del cliente.
    """

    cliente = obtener_cliente_actual(request.user)

    if not cliente:
        messages.error(request, 'Tu usuario no tiene pedidos como cliente.')
        return redirect('core:home')

    pedidos = Pedido.objects.filter(
        cliente=cliente
    ).prefetch_related(
        'detalles__producto'
    ).order_by('-fecha_pedido')

    return render(request, 'accounts/my_orders.html', {
        'cliente': cliente,
        'pedidos': pedidos,
    })


@login_required
def order_detail(request, pedido_id):
    """
    Muestra el detalle completo de un pedido del cliente.
    """

    cliente = obtener_cliente_actual(request.user)

    if not cliente:
        messages.error(request, 'Tu usuario no tiene pedidos como cliente.')
        return redirect('core:home')

    pedido = get_object_or_404(
        Pedido.objects.prefetch_related('detalles__producto'),
        id=pedido_id,
        cliente=cliente
    )

    venta = None
    comprobante = None
    entrega = None

    try:
        venta = pedido.venta
    except Venta.DoesNotExist:
        venta = None

    if venta:
        try:
            comprobante = venta.comprobante
        except Comprobante.DoesNotExist:
            comprobante = None

    try:
        entrega = pedido.entrega
    except Entrega.DoesNotExist:
        entrega = None

    context = {
        'cliente': cliente,
        'pedido': pedido,
        'venta': venta,
        'comprobante': comprobante,
        'entrega': entrega,
    }

    return render(request, 'accounts/order_detail.html', context)