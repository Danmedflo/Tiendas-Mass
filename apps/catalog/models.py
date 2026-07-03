"""
Archivo: models.py
Aplicación: catalog
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripción: Define los modelos de categorías, productos y control básico de inventario.
"""

from datetime import timedelta
from django.db import models
from django.utils import timezone


class Categoria(models.Model):
    """
    Modelo que clasifica los productos del catálogo.
    """

    nombre = models.CharField(max_length=80, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    """
    Modelo que representa los productos disponibles para venta online.
    """

    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True, null=True)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='productos'
    )
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(default=5)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['nombre']
        indexes = [
            models.Index(fields=['nombre']),
            models.Index(fields=['codigo']),
        ]

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'

    def esta_disponible(self):
        """
        Valida si el producto puede mostrarse y venderse.
        """
        return self.activo and self.stock > 0

    def tiene_stock_bajo(self):
        """
        Verifica si el stock actual está por debajo del mínimo permitido.
        """
        return self.stock <= self.stock_minimo

    def esta_por_vencer(self):
        """
        Verifica si el producto vence dentro de los próximos 7 días.
        """
        if not self.fecha_vencimiento:
            return False

        fecha_limite = timezone.now().date() + timedelta(days=7)
        return self.fecha_vencimiento <= fecha_limite

    def descontar_stock(self, cantidad):
        """
        Descuenta stock del producto si existe cantidad suficiente.
        """
        if cantidad <= 0:
            return False

        if self.stock >= cantidad:
            self.stock -= cantidad
            self.save()
            return True

        return False