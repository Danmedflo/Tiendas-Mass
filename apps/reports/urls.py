"""
Archivo: urls.py
Aplicación: reports
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripción: Define las rutas para dashboard y reportes administrativos.
"""

from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('reportes/ventas/', views.sales_report, name='sales_report'),
    path('reportes/stock/', views.stock_report, name='stock_report'),
    path('reportes/pedidos/', views.orders_report, name='orders_report'),
    path('reportes/clientes/', views.customers_report, name='customers_report'),
]