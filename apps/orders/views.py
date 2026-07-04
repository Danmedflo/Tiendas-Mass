"""
Archivo: views.py
Aplicación: orders
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripción: Define las vistas para carrito de compras, actualización de cantidades,
eliminación de productos, checkout y confirmación de pedidos.
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from apps.catalog.models import Producto
from apps.accounts.models import Cliente

from .forms import CheckoutForm
from .models import DetallePedido, Pedido
from .services import (
    calcular_costo_envio,
    calcular_items_carrito,
    limpiar_carrito,
    obtener_carrito,
    guardar_carrito,
    validar_stock_carrito,
)


@login_required
def cart_detail(request):
    """
    Muestra el contenido actual del carrito.
    """
    carrito = obtener_carrito(request)
    resumen = calcular_items_carrito(carrito)

    return render(request, 'orders/cart_detail.html', resumen)


@login_required
def add_to_cart(request, producto_id):
    """
    Agrega un producto al carrito o incrementa su cantidad.
    """
    producto = get_object_or_404(Producto, id=producto_id, activo=True)

    if producto.stock <= 0:
        messages.error(request, 'Este producto no tiene stock disponible.')
        return redirect('catalog:product_list')

    carrito = obtener_carrito(request)

    cantidad = int(request.POST.get('cantidad', 1))

    if cantidad <= 0:
        cantidad = 1

    producto_id_str = str(producto.id)
    cantidad_actual = int(carrito.get(producto_id_str, 0))
    nueva_cantidad = cantidad_actual + cantidad

    if nueva_cantidad > producto.stock:
        nueva_cantidad = producto.stock
        messages.warning(request, f'Solo hay {producto.stock} unidades disponibles de {producto.nombre}.')

    carrito[producto_id_str] = nueva_cantidad
    guardar_carrito(request, carrito)

    messages.success(request, f'{producto.nombre} fue agregado al carrito.')
    return redirect('orders:cart_detail')


@login_required
def update_cart(request, producto_id):
    """
    Actualiza la cantidad de un producto dentro del carrito.
    """
    producto = get_object_or_404(Producto, id=producto_id, activo=True)
    carrito = obtener_carrito(request)

    cantidad = int(request.POST.get('cantidad', 1))
    producto_id_str = str(producto.id)

    if cantidad <= 0:
        carrito.pop(producto_id_str, None)
        messages.success(request, 'Producto eliminado del carrito.')

    elif cantidad > producto.stock:
        carrito[producto_id_str] = producto.stock
        messages.warning(request, f'Solo hay {producto.stock} unidades disponibles.')

    else:
        carrito[producto_id_str] = cantidad
        messages.success(request, 'Cantidad actualizada correctamente.')

    guardar_carrito(request, carrito)

    return redirect('orders:cart_detail')


@login_required
def remove_from_cart(request, producto_id):
    """
    Elimina un producto específico del carrito.
    """
    carrito = obtener_carrito(request)
    producto_id_str = str(producto_id)

    if producto_id_str in carrito:
        carrito.pop(producto_id_str)
        guardar_carrito(request, carrito)
        messages.success(request, 'Producto eliminado del carrito.')

    return redirect('orders:cart_detail')


@login_required
def checkout(request):
    """
    Confirma la compra, registra el pedido y descuenta stock.
    """
    carrito = obtener_carrito(request)

    if not carrito:
        messages.error(request, 'Tu carrito está vacío.')
        return redirect('catalog:product_list')

    errores_stock = validar_stock_carrito(carrito)

    if errores_stock:
        for error in errores_stock:
            messages.error(request, error)
        return redirect('orders:cart_detail')

    cliente = get_object_or_404(Cliente, user=request.user)
    resumen = calcular_items_carrito(carrito)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)

        if form.is_valid():
            direccion_entrega = form.cleaned_data['direccion_entrega']
            distrito = form.cleaned_data['distrito']
            costo_envio = calcular_costo_envio(distrito)

            with transaction.atomic():
                pedido = Pedido.objects.create(
                    cliente=cliente,
                    estado=Pedido.ESTADO_CONFIRMADO,
                    direccion_entrega=direccion_entrega,
                    distrito=distrito,
                    costo_envio=costo_envio,
                )

                for item in resumen['items']:
                    producto = item['producto']
                    cantidad = item['cantidad']

                    DetallePedido.objects.create(
                        pedido=pedido,
                        producto=producto,
                        cantidad=cantidad,
                        precio_unitario=producto.precio,
                    )

                    producto.descontar_stock(cantidad)

                pedido.calcular_totales()

            limpiar_carrito(request)

            messages.success(request, 'Pedido registrado correctamente.')
            return redirect('orders:order_success', pedido_id=pedido.id)

    else:
        form = CheckoutForm(initial={
            'direccion_entrega': cliente.direccion,
            'distrito': cliente.distrito,
        })

    context = {
        'form': form,
        'items': resumen['items'],
        'subtotal': resumen['subtotal'],
        'igv': resumen['igv'],
        'total': resumen['total'],
    }

    return render(request, 'orders/checkout.html', context)


@login_required
def order_success(request, pedido_id):
    """
    Muestra la confirmación de un pedido registrado.
    """
    pedido = get_object_or_404(
        Pedido.objects.prefetch_related('detalles__producto'),
        id=pedido_id,
        cliente__user=request.user
    )

    return render(request, 'orders/order_success.html', {'pedido': pedido})