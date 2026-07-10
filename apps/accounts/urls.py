"""
Archivo: urls.py
Aplicación: accounts
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripción: Define las rutas de registro, login, logout, perfil y pedidos.
"""

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('registro/', views.register_client, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('perfil/', views.profile, name='profile'),
    path('perfil/editar/', views.edit_profile, name='edit_profile'),
    path('mis-pedidos/', views.my_orders, name='my_orders'),
    path('mis-pedidos/<int:pedido_id>/', views.order_detail, name='order_detail'),
]