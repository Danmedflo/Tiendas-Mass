"""
Archivo: views.py
Aplicación: catalog
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripción: Define vistas públicas del catálogo y vistas administrativas de gestión de productos.
"""

import csv
from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F, Q, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from apps.accounts.models import PerfilUsuario

from .forms import CategoriaAdminForm, ImportarProductosForm, ProductoAdminForm
from .models import Categoria, Producto


def usuario_es_administrador(user):
    """
    Valida si el usuario puede gestionar el catálogo.
    """

    if user.is_staff or user.is_superuser:
        return True

    try:
        return user.perfil.rol == PerfilUsuario.ROL_ADMIN
    except Exception:
        return False


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


@login_required
def admin_product_catalog(request):
    """
    Vista administrativa para gestionar productos del catálogo.
    """

    if not usuario_es_administrador(request.user):
        messages.error(request, 'No tienes permiso para gestionar el catálogo.')
        return redirect('core:home')

    productos = Producto.objects.select_related('categoria').all()
    categorias = Categoria.objects.all().order_by('nombre')

    busqueda = request.GET.get('q', '').strip()
    categoria_id = request.GET.get('categoria', '')
    estado = request.GET.get('estado', '')
    stock = request.GET.get('stock', '')

    if busqueda:
        productos = productos.filter(
            Q(nombre__icontains=busqueda) |
            Q(codigo__icontains=busqueda) |
            Q(descripcion__icontains=busqueda)
        )

    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    if estado == 'activo':
        productos = productos.filter(activo=True)

    if estado == 'inactivo':
        productos = productos.filter(activo=False)

    if stock == 'disponible':
        productos = productos.filter(stock__gt=0)

    if stock == 'agotado':
        productos = productos.filter(stock=0)

    if stock == 'bajo':
        productos = productos.filter(stock__lte=F('stock_minimo'))

    productos = productos.order_by('nombre')

    total_productos = Producto.objects.count()
    total_categorias = Categoria.objects.count()
    total_stock = Producto.objects.aggregate(total=Sum('stock'))['total'] or 0
    stock_bajo = Producto.objects.filter(stock__lte=F('stock_minimo')).count()

    import_form = ImportarProductosForm()

    context = {
        'productos': productos,
        'categorias': categorias,
        'busqueda': busqueda,
        'categoria_id': categoria_id,
        'estado': estado,
        'stock': stock,
        'total_productos': total_productos,
        'total_categorias': total_categorias,
        'total_stock': total_stock,
        'stock_bajo': stock_bajo,
        'import_form': import_form,
    }

    return render(request, 'catalog/admin/catalog_admin.html', context)


@login_required
def product_create(request):
    """
    Permite crear un nuevo producto desde la vista administrativa.
    """

    if not usuario_es_administrador(request.user):
        messages.error(request, 'No tienes permiso para crear productos.')
        return redirect('core:home')

    if request.method == 'POST':
        form = ProductoAdminForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado correctamente.')
            return redirect('catalog:admin_product_catalog')

    else:
        form = ProductoAdminForm()

    return render(request, 'catalog/admin/product_form.html', {
        'form': form,
        'titulo': 'Nuevo producto',
        'boton': 'Crear producto',
    })


@login_required
def product_edit(request, producto_id):
    """
    Permite editar un producto existente.
    """

    if not usuario_es_administrador(request.user):
        messages.error(request, 'No tienes permiso para editar productos.')
        return redirect('core:home')

    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        form = ProductoAdminForm(request.POST, request.FILES, instance=producto)

        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado correctamente.')
            return redirect('catalog:admin_product_catalog')

    else:
        form = ProductoAdminForm(instance=producto)

    return render(request, 'catalog/admin/product_form.html', {
        'form': form,
        'producto': producto,
        'titulo': 'Editar producto',
        'boton': 'Guardar cambios',
    })


@login_required
def product_toggle_status(request, producto_id):
    """
    Activa o desactiva un producto.
    """

    if not usuario_es_administrador(request.user):
        messages.error(request, 'No tienes permiso para cambiar el estado del producto.')
        return redirect('core:home')

    producto = get_object_or_404(Producto, id=producto_id)
    producto.activo = not producto.activo
    producto.save()

    if producto.activo:
        messages.success(request, 'Producto activado correctamente.')
    else:
        messages.warning(request, 'Producto desactivado correctamente.')

    return redirect('catalog:admin_product_catalog')


@login_required
def product_delete(request, producto_id):
    """
    Desactiva un producto como acción de eliminación segura.
    """

    if not usuario_es_administrador(request.user):
        messages.error(request, 'No tienes permiso para eliminar productos.')
        return redirect('core:home')

    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        producto.activo = False
        producto.save()
        messages.warning(request, 'Producto eliminado del catálogo público.')
        return redirect('catalog:admin_product_catalog')

    return render(request, 'catalog/admin/product_confirm_delete.html', {
        'producto': producto,
    })


@login_required
def category_create(request):
    """
    Permite crear una categoría desde la gestión de catálogo.
    """

    if not usuario_es_administrador(request.user):
        messages.error(request, 'No tienes permiso para crear categorías.')
        return redirect('core:home')

    if request.method == 'POST':
        form = CategoriaAdminForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada correctamente.')
            return redirect('catalog:admin_product_catalog')

    else:
        form = CategoriaAdminForm()

    return render(request, 'catalog/admin/category_form.html', {
        'form': form,
        'titulo': 'Nueva categoría',
        'boton': 'Crear categoría',
    })


@login_required
def export_products_csv(request):
    """
    Exporta los productos a un archivo CSV.
    """

    if not usuario_es_administrador(request.user):
        messages.error(request, 'No tienes permiso para exportar productos.')
        return redirect('core:home')

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="productos_tienda_mass.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'codigo',
        'nombre',
        'categoria',
        'precio',
        'stock',
        'stock_minimo',
        'estado',
        'fecha_vencimiento',
    ])

    productos = Producto.objects.select_related('categoria').order_by('nombre')

    for producto in productos:
        writer.writerow([
            producto.codigo,
            producto.nombre,
            producto.categoria.nombre,
            producto.precio,
            producto.stock,
            producto.stock_minimo,
            'Activo' if producto.activo else 'Inactivo',
            producto.fecha_vencimiento or '',
        ])

    return response


@login_required
def import_products_csv(request):
    """
    Importa productos desde un archivo CSV.
    """

    if not usuario_es_administrador(request.user):
        messages.error(request, 'No tienes permiso para importar productos.')
        return redirect('core:home')

    if request.method != 'POST':
        return redirect('catalog:admin_product_catalog')

    form = ImportarProductosForm(request.POST, request.FILES)

    if not form.is_valid():
        messages.error(request, 'Debes seleccionar un archivo CSV válido.')
        return redirect('catalog:admin_product_catalog')

    archivo = request.FILES['archivo']

    try:
        contenido = archivo.read().decode('utf-8-sig').splitlines()
        lector = csv.DictReader(contenido)

        creados = 0
        actualizados = 0

        for fila in lector:
            codigo = (fila.get('codigo') or '').strip()
            nombre = (fila.get('nombre') or '').strip()
            categoria_nombre = (fila.get('categoria') or 'Sin categoría').strip()

            if not codigo or not nombre:
                continue

            categoria, _ = Categoria.objects.get_or_create(
                nombre=categoria_nombre,
                defaults={'descripcion': 'Categoría importada desde CSV.', 'activo': True}
            )

            try:
                precio = Decimal(str(fila.get('precio') or '0').replace(',', '.'))
            except InvalidOperation:
                precio = Decimal('0.00')

            try:
                stock = int(fila.get('stock') or 0)
            except ValueError:
                stock = 0

            try:
                stock_minimo = int(fila.get('stock_minimo') or 5)
            except ValueError:
                stock_minimo = 5

            activo_texto = str(fila.get('activo') or 'activo').lower()
            activo = activo_texto in ['1', 'true', 'si', 'sí', 'activo', 'activa']

            producto, creado = Producto.objects.update_or_create(
                codigo=codigo,
                defaults={
                    'nombre': nombre,
                    'descripcion': fila.get('descripcion') or '',
                    'categoria': categoria,
                    'precio': precio,
                    'stock': stock,
                    'stock_minimo': stock_minimo,
                    'activo': activo,
                }
            )

            if creado:
                creados += 1
            else:
                actualizados += 1

        messages.success(
            request,
            f'Importación completada. Creados: {creados}. Actualizados: {actualizados}.'
        )

    except Exception as error:
        messages.error(request, f'No se pudo importar el archivo: {error}')

    return redirect('catalog:admin_product_catalog')