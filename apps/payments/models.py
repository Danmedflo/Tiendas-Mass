"""
Archivo: models.py
Aplicación: payments
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripción: Define los modelos de pagos, ventas y comprobantes digitales simulados.
"""

from uuid import uuid4
from django.db import models


class Pago(models.Model):
    """
    Modelo que registra la información de pago de un pedido.
    """

    METODO_YAPE = 'YAPE'
    METODO_PLIN = 'PLIN'
    METODO_TARJETA = 'TARJETA'
    METODO_TRANSFERENCIA = 'TRANSFERENCIA'
    METODO_CONTRA_ENTREGA = 'CONTRA_ENTREGA'

    METODOS = [
        (METODO_YAPE, 'Yape'),
        (METODO_PLIN, 'Plin'),
        (METODO_TARJETA, 'Tarjeta'),
        (METODO_TRANSFERENCIA, 'Transferencia bancaria'),
        (METODO_CONTRA_ENTREGA, 'Pago contra entrega'),
    ]

    ESTADO_PENDIENTE = 'PENDIENTE'
    ESTADO_APROBADO = 'APROBADO'
    ESTADO_RECHAZADO = 'RECHAZADO'

    ESTADOS = [
        (ESTADO_PENDIENTE, 'Pendiente'),
        (ESTADO_APROBADO, 'Aprobado'),
        (ESTADO_RECHAZADO, 'Rechazado'),
    ]

    pedido = models.OneToOneField(
        'orders.Pedido',
        on_delete=models.CASCADE,
        related_name='pago'
    )
    metodo_pago = models.CharField(max_length=30, choices=METODOS)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADOS, default=ESTADO_PENDIENTE)
    referencia = models.CharField(max_length=50, unique=True, blank=True)
    fecha_pago = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        ordering = ['-fecha_pago']

    def __str__(self):
        return f'{self.pedido.numero_pedido} - {self.metodo_pago}'

    def save(self, *args, **kwargs):
        """
        Genera referencia única para identificar la transacción.
        """
        if not self.referencia:
            self.referencia = f'PAY-{uuid4().hex[:10].upper()}'

        super().save(*args, **kwargs)


class Venta(models.Model):
    """
    Modelo que registra una venta confirmada.
    """

    TIPO_BOLETA = 'BOLETA'
    TIPO_FACTURA = 'FACTURA'

    TIPOS_COMPROBANTE = [
        (TIPO_BOLETA, 'Boleta'),
        (TIPO_FACTURA, 'Factura'),
    ]

    pedido = models.OneToOneField(
        'orders.Pedido',
        on_delete=models.PROTECT,
        related_name='venta'
    )
    empleado = models.ForeignKey(
        'accounts.Empleado',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ventas'
    )
    numero_comprobante = models.CharField(max_length=30, unique=True, blank=True)
    tipo_comprobante = models.CharField(
        max_length=20,
        choices=TIPOS_COMPROBANTE,
        default=TIPO_BOLETA
    )
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    igv = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=30)
    fecha_venta = models.DateTimeField(auto_now_add=True)
    activa = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['-fecha_venta']

    def __str__(self):
        return self.numero_comprobante or f'Venta #{self.id}'

    def save(self, *args, **kwargs):
        """
        Genera número de comprobante interno para la venta.
        """
        if not self.numero_comprobante:
            self.numero_comprobante = f'COMP-{uuid4().hex[:8].upper()}'

        super().save(*args, **kwargs)


class Comprobante(models.Model):
    """
    Modelo que representa un comprobante digital simulado.
    """

    venta = models.OneToOneField(
        Venta,
        on_delete=models.CASCADE,
        related_name='comprobante'
    )
    tipo = models.CharField(max_length=20, choices=Venta.TIPOS_COMPROBANTE)
    serie = models.CharField(max_length=10, default='B001')
    numero = models.CharField(max_length=20, unique=True, blank=True)
    archivo_pdf = models.FileField(upload_to='comprobantes/', blank=True, null=True)
    email_enviado = models.BooleanField(default=False)
    fecha_emision = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Comprobante'
        verbose_name_plural = 'Comprobantes'
        ordering = ['-fecha_emision']

    def __str__(self):
        return f'{self.serie}-{self.numero}'

    def save(self, *args, **kwargs):
        """
        Genera número interno para el comprobante.
        """
        if not self.numero:
            self.numero = uuid4().hex[:8].upper()

        super().save(*args, **kwargs)