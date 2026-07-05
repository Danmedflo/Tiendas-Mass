"""
Archivo: urls.py
Aplicación: payments
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripción: Define las rutas para pagos simulados, ventas, comprobantes y QR.
"""

from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('pedido/<int:pedido_id>/pago/', views.process_payment, name='process_payment'),
    path('pedido/<int:pedido_id>/pago/qr/', views.payment_qr, name='payment_qr'),
    path('pedido/<int:pedido_id>/pago/exito/', views.payment_success, name='payment_success'),
    path('venta/<int:venta_id>/comprobante/', views.receipt_detail, name='receipt_detail'),
]