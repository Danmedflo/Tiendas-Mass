"""
Archivo: apps.py
Aplicaci?n: payments
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripci?n: Gesti?n de pagos, ventas, IGV y comprobantes.
"""

from django.apps import AppConfig


class PaymentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.payments"
