"""
Archivo: apps.py
Aplicaci?n: catalog
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripci?n: Gesti?n de categor?as, productos, cat?logo e inventario.
"""

from django.apps import AppConfig


class CatalogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.catalog"
