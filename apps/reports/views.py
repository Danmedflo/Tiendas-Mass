"""
Archivo: views.py
Aplicación: reports
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripción: Define el dashboard administrativo y los reportes del sistema.
"""

from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, F, Sum
from django.shortcuts import redirect, render
from django.utils import timezone

from apps.accounts.models import Cliente, PerfilUsuario
from apps.catalog.models import Producto
from apps.orders.models import Pedido
from apps.payments.models import Venta

from .models import ReporteGenerado


def usuario_es_administrador(user):
    """
    Valida si el usuario puede acceder a reportes administrativos.
    """
    if user.is_staff or user.is_superuser:
        return True

    try:
        return user.perfil.rol == PerfilUsuario.ROL_ADMIN
    except Exception:
        return False


@login_required
def dashboard(request):
    """
    Muestra el panel principal con indicadores generales del sistema.
    """

    if not usuario_es_administrador(request.user):
        messages.error(request, 'No tienes permiso para acceder al dashboard administrativo.')
        return redirect('core:home')

    hoy = timezone.now().date()

    total_ventas = Venta.objects.filter(activa=True).aggregate(
        total=Sum('total')
    )['total'] or Decimal('0.00')

    ventas_hoy = Venta.objects.filter(
        activa=True,
        fecha_venta__date=hoy
    ).aggregate(
        total=Sum('total')
    )['total'] or Decimal('0.00')

    cantidad_pedidos = Pedido.objects.count()
    pedidos_pendientes = Pedido.objects.exclude(
        estado__in=[Pedido.ESTADO_ENTREGADO, Pedido.ESTADO_CANCELADO]
    ).count()

    productos_activos = Producto.objects.filter(activo=True).count()

    productos_stock_bajo = Producto.objects.filter(
        activo=True,
        stock__lte=F('stock_minimo')
    ).select_related('categoria')[:8]

    pedidos_recientes = Pedido.objects.select_related('cliente').order_by('-fecha_pedido')[:8]

    ventas_por_metodo = Venta.objects.filter(activa=True).values('metodo_pago').annotate(
        cantidad=Count('id'),
        total=Sum('total')
    ).order_by('-total')

    context = {
        'total_ventas': total_ventas,
        'ventas_hoy': ventas_hoy,
        'cantidad_pedidos': cantidad_pedidos,
        'pedidos_pendientes': pedidos_pendientes,
        'productos_activos': productos_activos,
        'productos_stock_bajo': productos_stock_bajo,
        'pedidos_recientes': pedidos_recientes,
        'ventas_por_metodo': ventas_por_metodo,
    }

    return render(request, 'reports/dashboard.html', context)


@login_required
def sales_report(request):
    """
    Reporte de ventas filtrado por rango de fechas.
    """

    if not usuario_es_administrador(request.user):
        messages.error(request, 'No tienes permiso para ver reportes.')
        return redirect('core:home')

    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    ventas = Venta.objects.select_related(
        'pedido',
        'pedido__cliente'
    ).filter(activa=True).order_by('-fecha_venta')

    if fecha_inicio:
        ventas = ventas.filter(fecha_venta__date__gte=fecha_inicio)

    if fecha_fin:
        ventas = ventas.filter(fecha_venta__date__lte=fecha_fin)

    total_vendido = ventas.aggregate(total=Sum('total'))['total'] or Decimal('0.00')
    cantidad_ventas = ventas.count()

    if request.GET.get('guardar') == '1':
        ReporteGenerado.objects.create(
            usuario=request.user,
            tipo=ReporteGenerado.TIPO_VENTAS,
            fecha_inicio=fecha_inicio or None,
            fecha_fin=fecha_fin or None,
            descripcion='Reporte de ventas generado desde el dashboard.'
        )
        messages.success(request, 'Reporte de ventas registrado correctamente.')

    return render(request, 'reports/sales_report.html', {
        'ventas': ventas,
        'total_vendido': total_vendido,
        'cantidad_ventas': cantidad_ventas,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    })


@login_required
def stock_report(request):
    """
    Reporte de productos con stock bajo y control de inventario.
    """

    if not usuario_es_administrador(request.user):
        messages.error(request, 'No tienes permiso para ver reportes.')
        return redirect('core:home')

    productos = Producto.objects.select_related('categoria').filter(activo=True).order_by('stock')
    stock_bajo = productos.filter(stock__lte=F('stock_minimo'))

    valor_inventario = Decimal('0.00')

    for producto in productos:
        valor_inventario += producto.precio * producto.stock

    if request.GET.get('guardar') == '1':
        ReporteGenerado.objects.create(
            usuario=request.user,
            tipo=ReporteGenerado.TIPO_STOCK,
            descripcion='Reporte de stock generado desde el dashboard.'
        )
        messages.success(request, 'Reporte de stock registrado correctamente.')

    return render(request, 'reports/stock_report.html', {
        'productos': productos,
        'stock_bajo': stock_bajo,
        'valor_inventario': valor_inventario,
    })


@login_required
def orders_report(request):
    """
    Reporte de pedidos agrupados por estado.
    """

    if not usuario_es_administrador(request.user):
        messages.error(request, 'No tienes permiso para ver reportes.')
        return redirect('core:home')

    pedidos = Pedido.objects.select_related('cliente').order_by('-fecha_pedido')

    resumen_estados = Pedido.objects.values('estado').annotate(
        cantidad=Count('id')
    ).order_by('estado')

    if request.GET.get('guardar') == '1':
        ReporteGenerado.objects.create(
            usuario=request.user,
            tipo=ReporteGenerado.TIPO_ENTREGAS,
            descripcion='Reporte de pedidos y entregas generado desde el dashboard.'
        )
        messages.success(request, 'Reporte de pedidos registrado correctamente.')

    return render(request, 'reports/orders_report.html', {
        'pedidos': pedidos,
        'resumen_estados': resumen_estados,
    })


@login_required
def customers_report(request):
    """
    Reporte de clientes registrados y cantidad de pedidos realizados.
    """

    if not usuario_es_administrador(request.user):
        messages.error(request, 'No tienes permiso para ver reportes.')
        return redirect('core:home')

    clientes = Cliente.objects.annotate(
        cantidad_pedidos=Count('pedidos')
    ).order_by('-fecha_registro')

    if request.GET.get('guardar') == '1':
        ReporteGenerado.objects.create(
            usuario=request.user,
            tipo=ReporteGenerado.TIPO_CLIENTES,
            descripcion='Reporte de clientes generado desde el dashboard.'
        )
        messages.success(request, 'Reporte de clientes registrado correctamente.')

    return render(request, 'reports/customers_report.html', {
        'clientes': clientes,
    })