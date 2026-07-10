"""
Archivo: urls.py
Aplicación: support
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripción: Define rutas para tickets de soporte e incidencias.
"""

from django.urls import path
from . import views

app_name = 'support'

urlpatterns = [
    path('soporte/nuevo/', views.create_ticket, name='create_ticket'),
    path('soporte/mis-tickets/', views.my_tickets, name='my_tickets'),
    path('soporte/ticket/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),

    path('soporte/admin/', views.admin_ticket_list, name='admin_ticket_list'),
    path('soporte/admin/ticket/<int:ticket_id>/', views.admin_ticket_detail, name='admin_ticket_detail'),
]