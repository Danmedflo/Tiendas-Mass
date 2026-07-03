"""
Archivo: apps.py
Aplicaci?n: delivery
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripci?n: Gesti?n de repartidores, zonas y entregas.
"""

from django.apps import AppConfig


class DeliveryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.delivery"
