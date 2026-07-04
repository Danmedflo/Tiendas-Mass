"""
Archivo: services.py
Aplicación: orders
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripción: Contiene funciones de apoyo para gestionar carrito, cálculos de compra,
validación de stock y costos de envío.
"""

from decimal import Decimal

from apps.catalog.models import Producto


CART_SESSION_KEY = 'cart'


def obtener_carrito(request):
    """
    Obtiene el carrito guardado en la sesión del usuario.
    """
    return request.session.get(CART_SESSION_KEY, {})


def guardar_carrito(request, carrito):
    """
    Guarda el carrito actualizado dentro de la sesión.
    """
    request.session[CART_SESSION_KEY] = carrito
    request.session.modified = True


def limpiar_carrito(request):
    """
    Elimina todos los productos del carrito.
    """
    request.session[CART_SESSION_KEY] = {}
    request.session.modified = True


def calcular_costo_envio(distrito):
    """
    Calcula el costo de envío según el distrito ingresado.
    Simula tarifas diferenciadas por zona.
    """
    distrito = distrito.lower().strip()

    tarifas = {
        'lima': Decimal('5.00'),
        'miraflores': Decimal('7.00'),
        'san isidro': Decimal('7.00'),
        'los olivos': Decimal('8.00'),
        'san juan de lurigancho': Decimal('9.00'),
        'villa el salvador': Decimal('9.00'),
        'ate': Decimal('8.50'),
        'comas': Decimal('8.00'),
    }

    return tarifas.get(distrito, Decimal('10.00'))


def calcular_items_carrito(carrito):
    """
    Convierte los productos guardados en sesión en información lista para mostrar.
    """
    items = []
    subtotal = Decimal('0.00')

    for producto_id, cantidad in carrito.items():
        try:
            producto = Producto.objects.get(id=producto_id, activo=True)
            cantidad = int(cantidad)

            item_subtotal = producto.precio * cantidad
            subtotal += item_subtotal

            items.append({
                'producto': producto,
                'cantidad': cantidad,
                'subtotal': item_subtotal,
            })

        except Producto.DoesNotExist:
            continue

    igv = subtotal * Decimal('0.18')
    total = subtotal + igv

    return {
        'items': items,
        'subtotal': subtotal,
        'igv': igv,
        'total': total,
    }


def validar_stock_carrito(carrito):
    """
    Valida si todos los productos del carrito tienen stock suficiente.
    """
    errores = []

    for producto_id, cantidad in carrito.items():
        try:
            producto = Producto.objects.get(id=producto_id, activo=True)
            cantidad = int(cantidad)

            if producto.stock < cantidad:
                errores.append(
                    f'El producto {producto.nombre} solo tiene {producto.stock} unidades disponibles.'
                )

        except Producto.DoesNotExist:
            errores.append('Uno de los productos del carrito ya no está disponible.')

    return errores