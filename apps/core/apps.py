"""
Archivo: apps.py
Aplicaci?n: core
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripci?n: Configuraci?n principal de p?ginas generales del sistema.
"""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"
