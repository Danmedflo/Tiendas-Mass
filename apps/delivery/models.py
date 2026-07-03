"""
Archivo: models.py
Aplicación: delivery
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripción: Define los modelos de repartidores, zonas y entregas a domicilio.
"""

from django.db import models


class Repartidor(models.Model):
    """
    Modelo que representa a un empleado encargado de entregas.
    """

    ESTADO_DISPONIBLE = 'DISPONIBLE'
    ESTADO_OCUPADO = 'OCUPADO'
    ESTADO_INACTIVO = 'INACTIVO'

    ESTADOS = [
        (ESTADO_DISPONIBLE, 'Disponible'),
        (ESTADO_OCUPADO, 'Ocupado'),
        (ESTADO_INACTIVO, 'Inactivo'),
    ]

    empleado = models.OneToOneField(
        'accounts.Empleado',
        on_delete=models.CASCADE,
        related_name='repartidor'
    )
    zona = models.CharField(max_length=100)
    licencia_conducir = models.CharField(max_length=30, blank=True, null=True)
    vehiculo = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default=ESTADO_DISPONIBLE)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Repartidor'
        verbose_name_plural = 'Repartidores'
        ordering = ['zona']

    def __str__(self):
        return f'{self.empleado.nombres} {self.empleado.apellidos} - {self.zona}'


class Entrega(models.Model):
    """
    Modelo que controla el proceso logístico de entrega del pedido.
    """

    ESTADO_ASIGNADA = 'ASIGNADA'
    ESTADO_EN_CAMINO = 'EN_CAMINO'
    ESTADO_ENTREGADA = 'ENTREGADA'
    ESTADO_FALLIDA = 'FALLIDA'
    ESTADO_REPROGRAMADA = 'REPROGRAMADA'

    ESTADOS = [
        (ESTADO_ASIGNADA, 'Asignada'),
        (ESTADO_EN_CAMINO, 'En camino'),
        (ESTADO_ENTREGADA, 'Entregada'),
        (ESTADO_FALLIDA, 'Fallida'),
        (ESTADO_REPROGRAMADA, 'Reprogramada'),
    ]

    pedido = models.OneToOneField(
        'orders.Pedido',
        on_delete=models.CASCADE,
        related_name='entrega'
    )
    repartidor = models.ForeignKey(
        Repartidor,
        on_delete=models.PROTECT,
        related_name='entregas'
    )
    estado = models.CharField(max_length=20, choices=ESTADOS, default=ESTADO_ASIGNADA)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateTimeField(blank=True, null=True)
    observacion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Entrega'
        verbose_name_plural = 'Entregas'
        ordering = ['-fecha_asignacion']

    def __str__(self):
        return f'Entrega {self.pedido.numero_pedido} - {self.estado}'