"""
Archivo: views.py
Aplicación: delivery
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripción: Define las vistas para seguimiento y actualización de entregas.
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.orders.models import Pedido
from .forms import ActualizarEntregaForm
from .models import Entrega, Repartidor


@login_required
def delivery_tracking(request, pedido_id):
    """
    Permite al cliente ver el seguimiento de entrega de su pedido.
    """

    pedido = get_object_or_404(
        Pedido.objects.select_related('cliente'),
        id=pedido_id,
        cliente__user=request.user
    )

    entrega = getattr(pedido, 'entrega', None)

    return render(request, 'delivery/tracking.html', {
        'pedido': pedido,
        'entrega': entrega,
    })


@login_required
def delivery_assigned_list(request):
    """
    Muestra al repartidor las entregas que tiene asignadas.
    """

    try:
        repartidor = request.user.empleado.repartidor
    except Exception:
        messages.error(request, 'Tu usuario no está vinculado a un repartidor.')
        return redirect('core:home')

    entregas = Entrega.objects.select_related(
        'pedido',
        'pedido__cliente',
        'repartidor'
    ).filter(
        repartidor=repartidor
    ).order_by('-fecha_asignacion')

    return render(request, 'delivery/assigned_list.html', {
        'repartidor': repartidor,
        'entregas': entregas,
    })


@login_required
def update_delivery_status(request, entrega_id):
    """
    Permite al repartidor actualizar el estado de una entrega.
    """

    try:
        repartidor = request.user.empleado.repartidor
    except Exception:
        messages.error(request, 'Tu usuario no está vinculado a un repartidor.')
        return redirect('core:home')

    entrega = get_object_or_404(
        Entrega.objects.select_related('pedido'),
        id=entrega_id,
        repartidor=repartidor
    )

    if request.method == 'POST':
        form = ActualizarEntregaForm(request.POST)

        if form.is_valid():
            nuevo_estado = form.cleaned_data['estado']
            observacion = form.cleaned_data.get('observacion') or ''

            entrega.estado = nuevo_estado
            entrega.observacion = observacion

            if nuevo_estado == Entrega.ESTADO_EN_CAMINO:
                entrega.pedido.estado = Pedido.ESTADO_EN_CAMINO

            elif nuevo_estado == Entrega.ESTADO_ENTREGADA:
                entrega.fecha_entrega = timezone.now()
                entrega.pedido.estado = Pedido.ESTADO_ENTREGADO
                repartidor.estado = Repartidor.ESTADO_DISPONIBLE
                repartidor.save()

            elif nuevo_estado in [Entrega.ESTADO_FALLIDA, Entrega.ESTADO_REPROGRAMADA]:
                repartidor.estado = Repartidor.ESTADO_DISPONIBLE
                repartidor.save()

            entrega.pedido.save()
            entrega.save()

            messages.success(request, 'Estado de entrega actualizado correctamente.')
            return redirect('delivery:assigned_list')

    else:
        form = ActualizarEntregaForm(initial={
            'estado': entrega.estado,
            'observacion': entrega.observacion,
        })

    return render(request, 'delivery/update_status.html', {
        'form': form,
        'entrega': entrega,
    })