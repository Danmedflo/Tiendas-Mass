"""
Archivo: urls.py
Aplicación: catalog
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripción: Define las rutas del catálogo de productos.
"""

from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('productos/', views.product_list, name='product_list'),
    path('productos/<int:producto_id>/', views.product_detail, name='product_detail'),
]