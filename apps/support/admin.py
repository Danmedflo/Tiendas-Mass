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
    list_display = ('asunto', 'usuario', 'tipo_problema', 'estado', 'prioridad', 'fecha_creacion')
    list_filter = ('estado', 'prioridad', 'tipo_problema')
    search_fields = ('asunto', 'descripcion', 'usuario__username')