"""
Archivo: admin.py
Aplicación: support
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripción: Configura la administración de tickets de soporte.
"""

from django.contrib import admin
from .models import TicketSoporte


@admin.register(TicketSoporte)
class TicketSoporteAdmin(admin.ModelAdmin):
    list_display = (
        'asunto',
        'usuario',
        'tipo_problema',
        'estado',
        'prioridad',
        'fecha_creacion',
        'fecha_cierre',
    )
    list_filter = ('estado', 'prioridad', 'tipo_problema', 'fecha_creacion')
    search_fields = (
        'asunto',
        'descripcion',
        'respuesta',
        'usuario__username',
        'usuario__email',
        'pedido__numero_pedido',
    )
    readonly_fields = ('fecha_creacion',)