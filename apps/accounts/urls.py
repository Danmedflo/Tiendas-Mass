"""
Archivo: urls.py
Aplicación: accounts
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripción: Define las rutas de registro, login y logout.
"""

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('registro/', views.register_client, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]