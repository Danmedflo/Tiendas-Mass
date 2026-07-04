"""
Archivo: admin.py
Aplicación: catalog
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripción: Configura la administración de categorías y productos.
"""

from django.contrib import admin
from .models import Categoria, Producto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre',)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        'codigo',
        'nombre',
        'categoria',
        'precio',
        'stock',
        'stock_minimo',
        'fecha_vencimiento',
        'activo',
    )
    list_filter = ('categoria', 'activo')
    search_fields = ('codigo', 'nombre')
    list_editable = ('precio', 'stock', 'stock_minimo', 'activo')