"""
Archivo: views.py
Aplicación: catalog
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripción: Define las vistas para consultar productos, aplicar filtros y ver detalles.
"""

from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Categoria, Producto


def product_list(request):
    """
    Muestra el catálogo de productos activos con búsqueda, filtros y ordenamiento.
    """

    productos = Producto.objects.select_related('categoria').filter(activo=True)
    categorias = Categoria.objects.filter(activo=True)

    busqueda = request.GET.get('q', '').strip()
    categoria_id = request.GET.get('categoria', '')
    disponibilidad = request.GET.get('disponibilidad', '')
    ordenar = request.GET.get('ordenar', 'nombre')

    if busqueda:
        productos = productos.filter(
            Q(nombre__icontains=busqueda) |
            Q(codigo__icontains=busqueda) |
            Q(descripcion__icontains=busqueda)
        )

    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    if disponibilidad == 'disponible':
        productos = productos.filter(stock__gt=0)

    if disponibilidad == 'agotado':
        productos = productos.filter(stock=0)

    ordenamientos_validos = {
        'nombre': 'nombre',
        'precio_menor': 'precio',
        'precio_mayor': '-precio',
        'stock': '-stock',
        'recientes': '-fecha_creacion',
    }

    productos = productos.order_by(ordenamientos_validos.get(ordenar, 'nombre'))

    context = {
        'productos': productos,
        'categorias': categorias,
        'busqueda': busqueda,
        'categoria_id': categoria_id,
        'disponibilidad': disponibilidad,
        'ordenar': ordenar,
    }

    return render(request, 'catalog/product_list.html', context)


def product_detail(request, producto_id):
    """
    Muestra la información detallada de un producto seleccionado.
    """

    producto = get_object_or_404(
        Producto.objects.select_related('categoria'),
        id=producto_id,
        activo=True
    )

    return render(request, 'catalog/product_detail.html', {'producto': producto})