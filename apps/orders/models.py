"""
Archivo: models.py
Aplicación: orders
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripción: Define los modelos de pedidos, detalle de pedido y proceso de compra.
"""

from decimal import Decimal
from uuid import uuid4
from django.db import models


class Pedido(models.Model):
    """
    Modelo que representa una orden de compra realizada por un cliente.
    """

    ESTADO_PENDIENTE = 'PENDIENTE'
    ESTADO_CONFIRMADO = 'CONFIRMADO'
    ESTADO_PAGADO = 'PAGADO'
    ESTADO_PREPARADO = 'PREPARADO'
    ESTADO_EN_CAMINO = 'EN_CAMINO'
    ESTADO_ENTREGADO = 'ENTREGADO'
    ESTADO_CANCELADO = 'CANCELADO'

    ESTADOS = [
        (ESTADO_PENDIENTE, 'Pendiente'),
        (ESTADO_CONFIRMADO, 'Confirmado'),
        (ESTADO_PAGADO, 'Pagado'),
        (ESTADO_PREPARADO, 'Preparado'),
        (ESTADO_EN_CAMINO, 'En camino'),
        (ESTADO_ENTREGADO, 'Entregado'),
        (ESTADO_CANCELADO, 'Cancelado'),
    ]

    cliente = models.ForeignKey(
        'accounts.Cliente',
        on_delete=models.PROTECT,
        related_name='pedidos'
    )
    empleado = models.ForeignKey(
        'accounts.Empleado',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pedidos_procesados'
    )
    numero_pedido = models.CharField(max_length=20, unique=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default=ESTADO_PENDIENTE)
    direccion_entrega = models.CharField(max_length=200)
    distrito = models.CharField(max_length=100)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    costo_envio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    igv = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-fecha_pedido']

    def __str__(self):
        return self.numero_pedido or f'Pedido #{self.id}'

    def save(self, *args, **kwargs):
        """
        Genera un número único de pedido cuando se crea por primera vez.
        """
        if not self.numero_pedido:
            self.numero_pedido = f'PED-{uuid4().hex[:8].upper()}'

        super().save(*args, **kwargs)

    def calcular_totales(self):
        """
        Calcula subtotal, IGV y total del pedido según los detalles registrados,
        redondeando todos los importes a dos decimales.
        """
        subtotal = sum(detalle.subtotal for detalle in self.detalles.all())

        self.subtotal = subtotal.quantize(Decimal('0.01'))
        self.igv = (self.subtotal * Decimal('0.18')).quantize(Decimal('0.01'))
        self.total = (self.subtotal + self.igv + self.costo_envio).quantize(Decimal('0.01'))

        self.save()


class DetallePedido(models.Model):
    """
    Modelo que almacena los productos incluidos en un pedido.
    """

    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name='detalles'
    )
    producto = models.ForeignKey(
        'catalog.Producto',
        on_delete=models.PROTECT,
        related_name='detalles_pedido'
    )
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Detalle de Pedido'
        verbose_name_plural = 'Detalles de Pedido'

    def __str__(self):
        return f'{self.producto.nombre} x {self.cantidad}'

    def save(self, *args, **kwargs):
        """
        Calcula el subtotal del producto dentro del pedido con dos decimales.
        """
        self.subtotal = (self.precio_unitario * self.cantidad).quantize(Decimal('0.01'))
        super().save(*args, **kwargs)