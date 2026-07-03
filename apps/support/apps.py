"""
Archivo: apps.py
Aplicaci?n: support
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripci?n: Gesti?n de incidencias, soporte t?cnico y mantenimiento.
"""

from django.apps import AppConfig


class SupportConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.support"
