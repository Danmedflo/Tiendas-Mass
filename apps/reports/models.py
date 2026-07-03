"""
Archivo: models.py
Aplicación: reports
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripción: Define el modelo para registrar reportes generados por el administrador.
"""

from django.contrib.auth.models import User
from django.db import models


class ReporteGenerado(models.Model):
    """
    Modelo que almacena el historial de reportes generados.
    """

    TIPO_VENTAS = 'VENTAS'
    TIPO_STOCK = 'STOCK'
    TIPO_ENTREGAS = 'ENTREGAS'
    TIPO_CLIENTES = 'CLIENTES'

    TIPOS = [
        (TIPO_VENTAS, 'Reporte de ventas'),
        (TIPO_STOCK, 'Reporte de stock'),
        (TIPO_ENTREGAS, 'Reporte de entregas'),
        (TIPO_CLIENTES, 'Reporte de clientes'),
    ]

    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reportes_generados'
    )
    tipo = models.CharField(max_length=20, choices=TIPOS)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    archivo = models.FileField(upload_to='reportes/', blank=True, null=True)
    fecha_generacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Reporte Generado'
        verbose_name_plural = 'Reportes Generados'
        ordering = ['-fecha_generacion']

    def __str__(self):
        return f'{self.get_tipo_display()} - {self.fecha_generacion.date()}'