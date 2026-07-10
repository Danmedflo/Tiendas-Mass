"""
Archivo: urls.py
Aplicación: catalog
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripción: Define rutas públicas y administrativas del catálogo.
"""

from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('productos/', views.product_list, name='product_list'),
    path('productos/<int:producto_id>/', views.product_detail, name='product_detail'),

    path('gestion/catalogo/', views.admin_product_catalog, name='admin_product_catalog'),
    path('gestion/catalogo/producto/nuevo/', views.product_create, name='product_create'),
    path('gestion/catalogo/producto/<int:producto_id>/editar/', views.product_edit, name='product_edit'),
    path('gestion/catalogo/producto/<int:producto_id>/estado/', views.product_toggle_status, name='product_toggle_status'),
    path('gestion/catalogo/producto/<int:producto_id>/eliminar/', views.product_delete, name='product_delete'),
    path('gestion/catalogo/categoria/nueva/', views.category_create, name='category_create'),
    path('gestion/catalogo/exportar/', views.export_products_csv, name='export_products_csv'),
    path('gestion/catalogo/importar/', views.import_products_csv, name='import_products_csv'),
]