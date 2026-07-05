"""
Archivo: forms.py
Aplicación: payments
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripción: Define formularios para procesar pagos simulados y seleccionar comprobante.
"""

from django import forms

from .models import Pago, Venta


class PagoSimuladoForm(forms.Form):
    """
    Formulario para simular el pago de un pedido.
    """

    metodo_pago = forms.ChoiceField(
        label='Método de pago',
        choices=Pago.METODOS
    )

    tipo_comprobante = forms.ChoiceField(
        label='Tipo de comprobante',
        choices=Venta.TIPOS_COMPROBANTE
    )

    numero_operacion = forms.CharField(
        label='Número de operación',
        max_length=50,
        required=False
    )

    observacion = forms.CharField(
        label='Observación',
        required=False,
        widget=forms.Textarea(attrs={'rows': 3})
    )