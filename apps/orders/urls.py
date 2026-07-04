"""
Archivo: urls.py
Aplicación: orders
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripción: Define las rutas del carrito, checkout y confirmación de pedidos.
"""

from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('carrito/', views.cart_detail, name='cart_detail'),
    path('carrito/agregar/<int:producto_id>/', views.add_to_cart, name='add_to_cart'),
    path('carrito/actualizar/<int:producto_id>/', views.update_cart, name='update_cart'),
    path('carrito/eliminar/<int:producto_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('pedido/<int:pedido_id>/confirmacion/', views.order_success, name='order_success'),
]