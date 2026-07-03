"""
Archivo: models.py
Aplicación: support
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripción: Define el modelo de tickets de soporte e incidencias técnicas.
"""

from django.contrib.auth.models import User
from django.db import models


class TicketSoporte(models.Model):
    """
    Modelo que registra incidencias o consultas de soporte técnico.
    """

    ESTADO_ABIERTO = 'ABIERTO'
    ESTADO_EN_PROCESO = 'EN_PROCESO'
    ESTADO_RESUELTO = 'RESUELTO'
    ESTADO_CERRADO = 'CERRADO'

    ESTADOS = [
        (ESTADO_ABIERTO, 'Abierto'),
        (ESTADO_EN_PROCESO, 'En proceso'),
        (ESTADO_RESUELTO, 'Resuelto'),
        (ESTADO_CERRADO, 'Cerrado'),
    ]

    PRIORIDAD_BAJA = 'BAJA'
    PRIORIDAD_MEDIA = 'MEDIA'
    PRIORIDAD_ALTA = 'ALTA'

    PRIORIDADES = [
        (PRIORIDAD_BAJA, 'Baja'),
        (PRIORIDAD_MEDIA, 'Media'),
        (PRIORIDAD_ALTA, 'Alta'),
    ]

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tickets_soporte'
    )
    pedido = models.ForeignKey(
        'orders.Pedido',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tickets_soporte'
    )
    asunto = models.CharField(max_length=150)
    descripcion = models.TextField()
    tipo_problema = models.CharField(max_length=100)
    estado = models.CharField(max_length=20, choices=ESTADOS, default=ESTADO_ABIERTO)
    prioridad = models.CharField(max_length=20, choices=PRIORIDADES, default=PRIORIDAD_MEDIA)
    respuesta = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_cierre = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Ticket de Soporte'
        verbose_name_plural = 'Tickets de Soporte'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f'{self.asunto} - {self.estado}'