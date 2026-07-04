"""
Archivo: forms.py
Aplicación: orders
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripción: Define formularios para confirmar datos de entrega en el checkout.
"""

from django import forms


class CheckoutForm(forms.Form):
    """
    Formulario para confirmar dirección de entrega antes de registrar el pedido.
    """

    direccion_entrega = forms.CharField(
        max_length=200,
        label='Dirección de entrega'
    )

    distrito = forms.CharField(
        max_length=100,
        label='Distrito'
    )

    observacion = forms.CharField(
        label='Observación',
        required=False,
        widget=forms.Textarea(attrs={'rows': 3})
    )