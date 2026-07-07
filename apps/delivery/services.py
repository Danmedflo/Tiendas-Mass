"""
Archivo: services.py
Aplicación: delivery
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripción: Contiene la lógica para asignar repartidores y crear entregas automáticamente.
"""

from django.db import transaction

from apps.orders.models import Pedido
from .models import Entrega, Repartidor


def buscar_repartidor_disponible(distrito):
    """
    Busca un repartidor disponible según la zona del pedido.
    Primero intenta encontrar coincidencia exacta con el distrito.
    Si no encuentra, toma cualquier repartidor disponible.
    """

    repartidor = Repartidor.objects.filter(
        activo=True,
        estado=Repartidor.ESTADO_DISPONIBLE,
        zona__iexact=distrito
    ).first()

    if repartidor:
        return repartidor

    return Repartidor.objects.filter(
        activo=True,
        estado=Repartidor.ESTADO_DISPONIBLE
    ).first()


def asignar_entrega_automatica(pedido):
    """
    Crea una entrega automática para un pedido pagado.
    Si existe repartidor disponible, lo asigna y cambia su estado a ocupado.
    """

    if hasattr(pedido, 'entrega'):
        return pedido.entrega

    repartidor = buscar_repartidor_disponible(pedido.distrito)

    if not repartidor:
        return None

    with transaction.atomic():
        entrega = Entrega.objects.create(
            pedido=pedido,
            repartidor=repartidor,
            estado=Entrega.ESTADO_ASIGNADA,
            observacion='Entrega asignada automáticamente después del pago.'
        )

        repartidor.estado = Repartidor.ESTADO_OCUPADO
        repartidor.save()

        pedido.estado = Pedido.ESTADO_PREPARADO
        pedido.save()

    return entrega