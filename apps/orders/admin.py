"""
Archivo: admin.py
Aplicación: orders
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripción: Configura la administración de pedidos y detalles de pedido.
"""

from django.contrib import admin
from .models import Pedido, DetallePedido


class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        'numero_pedido',
        'cliente',
        'estado',
        'subtotal',
        'igv',
        'costo_envio',
        'total',
        'fecha_pedido',
    )
    list_filter = ('estado', 'distrito', 'fecha_pedido')
    search_fields = ('numero_pedido', 'cliente__nombres', 'cliente__apellidos')
    inlines = [DetallePedidoInline]


@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'producto', 'cantidad', 'precio_unitario', 'subtotal')
    search_fields = ('pedido__numero_pedido', 'producto__nombre')