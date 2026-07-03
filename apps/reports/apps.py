"""
Archivo: apps.py
Aplicaci?n: reports
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripci?n: Gesti?n de dashboard, reportes y an?lisis.
"""

from django.apps import AppConfig


class ReportsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.reports"
