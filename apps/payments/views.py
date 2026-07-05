"""
Archivo: views.py
Aplicación: payments
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripción: Define las vistas para pagos simulados, registro de ventas y comprobantes.
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from apps.orders.models import Pedido

from .forms import PagoSimuladoForm
from .models import Comprobante, Pago, Venta

from io import BytesIO

import qrcode
from django.http import HttpResponse


@login_required
def process_payment(request, pedido_id):
    """
    Procesa un pago simulado para un pedido confirmado.
    """

    pedido = get_object_or_404(
        Pedido,
        id=pedido_id,
        cliente__user=request.user
    )

    if hasattr(pedido, 'pago') and pedido.pago.estado == Pago.ESTADO_APROBADO:
        messages.info(request, 'Este pedido ya tiene un pago aprobado.')
        return redirect('payments:payment_success', pedido_id=pedido.id)

    if request.method == 'POST':
        form = PagoSimuladoForm(request.POST)

        if form.is_valid():
            metodo_pago = form.cleaned_data['metodo_pago']
            tipo_comprobante = form.cleaned_data['tipo_comprobante']
            numero_operacion = form.cleaned_data.get('numero_operacion') or ''

            with transaction.atomic():
                pago = Pago.objects.create(
                    pedido=pedido,
                    metodo_pago=metodo_pago,
                    monto=pedido.total,
                    estado=Pago.ESTADO_APROBADO,
                )

                if numero_operacion:
                    pago.referencia = numero_operacion
                    pago.save()

                venta = Venta.objects.create(
                    pedido=pedido,
                    empleado=pedido.empleado,
                    tipo_comprobante=tipo_comprobante,
                    subtotal=pedido.subtotal,
                    igv=pedido.igv,
                    total=pedido.total,
                    metodo_pago=metodo_pago,
                    activa=True,
                )

                Comprobante.objects.create(
                    venta=venta,
                    tipo=tipo_comprobante,
                    serie='B001' if tipo_comprobante == Venta.TIPO_BOLETA else 'F001',
                    email_enviado=True,
                )

                pedido.estado = Pedido.ESTADO_PAGADO
                pedido.save()

            messages.success(request, 'Pago procesado correctamente. Se generó la venta y el comprobante.')
            return redirect('payments:payment_success', pedido_id=pedido.id)

    else:
        form = PagoSimuladoForm(initial={
            'metodo_pago': Pago.METODO_YAPE,
            'tipo_comprobante': Venta.TIPO_BOLETA,
        })

    context = {
        'pedido': pedido,
        'form': form,
    }

    return render(request, 'payments/payment_process.html', context)


@login_required
def payment_success(request, pedido_id):
    """
    Muestra el resultado exitoso del pago simulado.
    """

    pedido = get_object_or_404(
        Pedido.objects.select_related('cliente'),
        id=pedido_id,
        cliente__user=request.user
    )

    pago = get_object_or_404(Pago, pedido=pedido)
    venta = get_object_or_404(Venta, pedido=pedido)
    comprobante = get_object_or_404(Comprobante, venta=venta)

    context = {
        'pedido': pedido,
        'pago': pago,
        'venta': venta,
        'comprobante': comprobante,
    }

    return render(request, 'payments/payment_success.html', context)


@login_required
def receipt_detail(request, venta_id):
    """
    Muestra el comprobante digital simulado de una venta.
    """

    venta = get_object_or_404(
        Venta.objects.select_related('pedido', 'pedido__cliente'),
        id=venta_id,
        pedido__cliente__user=request.user
    )

    comprobante = get_object_or_404(Comprobante, venta=venta)

    context = {
        'venta': venta,
        'pedido': venta.pedido,
        'comprobante': comprobante,
    }

    return render(request, 'payments/receipt_detail.html', context)

@login_required
def payment_qr(request, pedido_id):
    """
    Genera un código QR simulado para pagos con Yape o Plin.
    """

    pedido = get_object_or_404(
        Pedido,
        id=pedido_id,
        cliente__user=request.user
    )

    metodo = request.GET.get('metodo', Pago.METODO_YAPE).upper()

    if metodo not in [Pago.METODO_YAPE, Pago.METODO_PLIN]:
        metodo = Pago.METODO_YAPE

    contenido_qr = (
        f"TIENDAS MASS\n"
        f"Metodo: {metodo}\n"
        f"Pedido: {pedido.numero_pedido}\n"
        f"Monto: S/ {pedido.total}\n"
        f"Celular comercio: 999888777\n"
        f"Concepto: Compra online Tiendas Mass"
    )

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4
    )
    qr.add_data(contenido_qr)
    qr.make(fit=True)

    imagen = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    imagen.save(buffer, format="PNG")
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type="image/png")