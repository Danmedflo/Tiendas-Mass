"""
Archivo: forms.py
Aplicación: catalog
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripción: Formularios para administración de productos y carga masiva.
"""

from django import forms

from .models import Categoria, Producto


class ProductoAdminForm(forms.ModelForm):
    """
    Formulario administrativo para crear y editar productos.
    """

    class Meta:
        model = Producto
        fields = [
            'codigo',
            'nombre',
            'descripcion',
            'categoria',
            'precio',
            'stock',
            'stock_minimo',
            'fecha_vencimiento',
            'imagen',
            'activo',
        ]

        widgets = {
            'codigo': forms.TextInput(attrs={'placeholder': 'Ejemplo: PROD001'}),
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre del producto'}),
            'descripcion': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Descripción breve del producto'}),
            'precio': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'stock': forms.NumberInput(attrs={'min': '0'}),
            'stock_minimo': forms.NumberInput(attrs={'min': '0'}),
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date'}),
        }


class CategoriaAdminForm(forms.ModelForm):
    """
    Formulario para crear categorías desde la gestión de catálogo.
    """

    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion', 'activo']

        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ejemplo: Bebidas'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descripción de la categoría'}),
        }


class ImportarProductosForm(forms.Form):
    """
    Formulario para importar productos desde un archivo CSV.
    """

    archivo = forms.FileField(
        label='Archivo CSV',
        help_text='Columnas sugeridas: codigo,nombre,categoria,precio,stock,stock_minimo,activo'
    )