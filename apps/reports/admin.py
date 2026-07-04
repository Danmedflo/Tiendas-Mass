"""
Archivo: admin.py
Aplicación: reports
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripción: Configura la administración de reportes generados.
"""

from django.contrib import admin
from .models import ReporteGenerado


@admin.register(ReporteGenerado)
class ReporteGeneradoAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'usuario', 'fecha_inicio', 'fecha_fin', 'fecha_generacion')
    list_filter = ('tipo', 'fecha_generacion')
    search_fields = ('descripcion', 'usuario__username')