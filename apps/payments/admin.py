"""
Archivo: admin.py
Aplicación: payments
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripción: Configura la administración de pagos, ventas y comprobantes.
"""

from django.contrib import admin
from .models import Pago, Venta, Comprobante


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = (
        'pedido',
        'metodo_pago',
        'monto',
        'estado',
        'referencia',
        'numero_operacion',
        'banco',
        'tarjeta_marca',
        'tarjeta_ultimos4',
        'fecha_pago',
    )
    list_filter = ('metodo_pago', 'estado', 'banco', 'tarjeta_marca')
    search_fields = (
        'pedido__numero_pedido',
        'referencia',
        'numero_operacion',
        'tarjeta_titular',
        'tarjeta_ultimos4',
    )


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = (
        'numero_comprobante',
        'pedido',
        'tipo_comprobante',
        'subtotal',
        'igv',
        'total',
        'metodo_pago',
        'fecha_venta',
        'activa',
    )
    list_filter = ('tipo_comprobante', 'metodo_pago', 'activa')
    search_fields = ('numero_comprobante', 'pedido__numero_pedido')


@admin.register(Comprobante)
class ComprobanteAdmin(admin.ModelAdmin):
    list_display = ('serie', 'numero', 'tipo', 'venta', 'email_enviado', 'fecha_emision')
    list_filter = ('tipo', 'email_enviado')
    search_fields = ('serie', 'numero', 'venta__numero_comprobante')