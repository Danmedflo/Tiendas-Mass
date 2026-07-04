"""
Archivo: admin.py
Aplicación: delivery
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripción: Configura la administración de repartidores y entregas.
"""

from django.contrib import admin
from .models import Repartidor, Entrega


@admin.register(Repartidor)
class RepartidorAdmin(admin.ModelAdmin):
    list_display = ('empleado', 'zona', 'vehiculo', 'estado', 'activo')
    list_filter = ('zona', 'estado', 'activo')
    search_fields = ('empleado__nombres', 'empleado__apellidos', 'zona')


@admin.register(Entrega)
class EntregaAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'repartidor', 'estado', 'fecha_asignacion', 'fecha_entrega')
    list_filter = ('estado', 'fecha_asignacion')
    search_fields = ('pedido__numero_pedido', 'repartidor__empleado__nombres')