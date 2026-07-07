"""
Archivo: urls.py
Aplicación: delivery
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripción: Define las rutas para seguimiento y gestión de entregas.
"""

from django.urls import path
from . import views

app_name = 'delivery'

urlpatterns = [
    path('pedido/<int:pedido_id>/seguimiento/', views.delivery_tracking, name='tracking'),
    path('repartidor/entregas/', views.delivery_assigned_list, name='assigned_list'),
    path('repartidor/entrega/<int:entrega_id>/actualizar/', views.update_delivery_status, name='update_status'),
]