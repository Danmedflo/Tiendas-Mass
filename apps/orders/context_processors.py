"""
Archivo: context_processors.py
Aplicación: orders
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripción: Permite mostrar información del carrito en todas las vistas.
"""

from .services import obtener_carrito


def cart_context(request):
    """
    Retorna la cantidad total de productos agregados al carrito.
    """

    carrito = obtener_carrito(request)
    cantidad_total = 0

    for cantidad in carrito.values():
        try:
            cantidad_total += int(cantidad)
        except (TypeError, ValueError):
            continue

    return {
        'cart_item_count': cantidad_total,
    }