"""
Archivo: views.py
Aplicación: core
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripción: Define las vistas generales del sistema, como la página principal.
"""

from django.shortcuts import render


def home(request):
    """
    Muestra la página principal del sistema Tiendas Mass.
    """
    return render(request, 'core/home.html')