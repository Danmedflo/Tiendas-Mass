"""
Archivo: views.py
Aplicación: support
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripción: Define vistas para creación, consulta y administración de tickets de soporte.
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.accounts.models import Cliente, PerfilUsuario
from apps.orders.models import Pedido

from .forms import ActualizarTicketAdminForm, TicketSoporteForm
from .models import TicketSoporte


def usuario_es_administrador(user):
    """
    Verifica si el usuario tiene permisos administrativos.
    """

    if user.is_staff or user.is_superuser:
        return True

    try:
        return user.perfil.rol == PerfilUsuario.ROL_ADMIN
    except Exception:
        return False


def obtener_cliente_actual(user):
    """
    Obtiene el cliente vinculado al usuario autenticado.
    """

    try:
        return user.cliente
    except Cliente.DoesNotExist:
        return None


@login_required
def create_ticket(request):
    """
    Permite al cliente crear un ticket de soporte.
    """

    cliente = obtener_cliente_actual(request.user)

    pedidos_queryset = Pedido.objects.none()

    if cliente:
        pedidos_queryset = Pedido.objects.filter(cliente=cliente).order_by('-fecha_pedido')

    if request.method == 'POST':
        form = TicketSoporteForm(
            request.POST,
            pedidos_queryset=pedidos_queryset
        )

        if form.is_valid():
            TicketSoporte.objects.create(
                usuario=request.user,
                pedido=form.cleaned_data.get('pedido'),
                asunto=form.cleaned_data['asunto'],
                descripcion=form.cleaned_data['descripcion'],
                tipo_problema=form.cleaned_data['tipo_problema'],
                estado=TicketSoporte.ESTADO_ABIERTO,
                prioridad=TicketSoporte.PRIORIDAD_MEDIA,
            )

            messages.success(request, 'Ticket registrado correctamente. Soporte revisará tu caso.')
            return redirect('support:my_tickets')

    else:
        form = TicketSoporteForm(pedidos_queryset=pedidos_queryset)

    return render(request, 'support/create_ticket.html', {
        'form': form,
    })


@login_required
def my_tickets(request):
    """
    Muestra los tickets creados por el usuario autenticado.
    """

    tickets = TicketSoporte.objects.select_related(
        'pedido'
    ).filter(
        usuario=request.user
    ).order_by('-fecha_creacion')

    return render(request, 'support/my_tickets.html', {
        'tickets': tickets,
    })


@login_required
def ticket_detail(request, ticket_id):
    """
    Muestra el detalle de un ticket creado por el usuario.
    """

    ticket = get_object_or_404(
        TicketSoporte.objects.select_related('pedido', 'usuario'),
        id=ticket_id,
        usuario=request.user
    )

    return render(request, 'support/ticket_detail.html', {
        'ticket': ticket,
    })


@login_required
def admin_ticket_list(request):
    """
    Muestra al administrador todos los tickets registrados.
    """

    if not usuario_es_administrador(request.user):
        messages.error(request, 'No tienes permiso para acceder a soporte administrativo.')
        return redirect('core:home')

    estado = request.GET.get('estado', '')
    prioridad = request.GET.get('prioridad', '')

    tickets = TicketSoporte.objects.select_related(
        'usuario',
        'pedido'
    ).order_by('-fecha_creacion')

    if estado:
        tickets = tickets.filter(estado=estado)

    if prioridad:
        tickets = tickets.filter(prioridad=prioridad)

    total_tickets = TicketSoporte.objects.count()
    abiertos = TicketSoporte.objects.filter(estado=TicketSoporte.ESTADO_ABIERTO).count()
    en_proceso = TicketSoporte.objects.filter(estado=TicketSoporte.ESTADO_EN_PROCESO).count()
    resueltos = TicketSoporte.objects.filter(estado=TicketSoporte.ESTADO_RESUELTO).count()

    context = {
        'tickets': tickets,
        'estado': estado,
        'prioridad': prioridad,
        'estados': TicketSoporte.ESTADOS,
        'prioridades': TicketSoporte.PRIORIDADES,
        'total_tickets': total_tickets,
        'abiertos': abiertos,
        'en_proceso': en_proceso,
        'resueltos': resueltos,
    }

    return render(request, 'support/admin_ticket_list.html', context)


@login_required
def admin_ticket_detail(request, ticket_id):
    """
    Permite al administrador revisar, responder y actualizar el estado del ticket.
    """

    if not usuario_es_administrador(request.user):
        messages.error(request, 'No tienes permiso para administrar tickets.')
        return redirect('core:home')

    ticket = get_object_or_404(
        TicketSoporte.objects.select_related('usuario', 'pedido'),
        id=ticket_id
    )

    if request.method == 'POST':
        form = ActualizarTicketAdminForm(request.POST)

        if form.is_valid():
            estado = form.cleaned_data['estado']
            prioridad = form.cleaned_data['prioridad']
            respuesta = form.cleaned_data.get('respuesta') or ''

            ticket.estado = estado
            ticket.prioridad = prioridad
            ticket.respuesta = respuesta

            if estado in [TicketSoporte.ESTADO_RESUELTO, TicketSoporte.ESTADO_CERRADO]:
                ticket.fecha_cierre = timezone.now()
            else:
                ticket.fecha_cierre = None

            ticket.save()

            messages.success(request, 'Ticket actualizado correctamente.')
            return redirect('support:admin_ticket_list')

    else:
        form = ActualizarTicketAdminForm(initial={
            'estado': ticket.estado,
            'prioridad': ticket.prioridad,
            'respuesta': ticket.respuesta,
        })

    return render(request, 'support/admin_ticket_detail.html', {
        'ticket': ticket,
        'form': form,
    })