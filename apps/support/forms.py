"""
Archivo: forms.py
Aplicación: support
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripción: Define formularios para registrar y administrar tickets de soporte.
"""

from django import forms

from apps.orders.models import Pedido
from .models import TicketSoporte


class TicketSoporteForm(forms.Form):
    """
    Formulario para que el cliente registre una incidencia o consulta.
    """

    TIPO_ENTREGA = 'Entrega'
    TIPO_PAGO = 'Pago'
    TIPO_PRODUCTO = 'Producto'
    TIPO_COMPROBANTE = 'Comprobante'
    TIPO_CUENTA = 'Cuenta de usuario'
    TIPO_OTRO = 'Otro'

    TIPOS_PROBLEMA = [
        (TIPO_ENTREGA, 'Problema con la entrega'),
        (TIPO_PAGO, 'Problema con el pago'),
        (TIPO_PRODUCTO, 'Producto equivocado o en mal estado'),
        (TIPO_COMPROBANTE, 'Consulta sobre comprobante'),
        (TIPO_CUENTA, 'Problema con mi cuenta'),
        (TIPO_OTRO, 'Otro'),
    ]

    pedido = forms.ModelChoiceField(
        label='Pedido relacionado',
        queryset=Pedido.objects.none(),
        required=False,
        empty_label='No está relacionado a un pedido'
    )

    tipo_problema = forms.ChoiceField(
        label='Tipo de problema',
        choices=TIPOS_PROBLEMA
    )

    asunto = forms.CharField(
        label='Asunto',
        max_length=150
    )

    descripcion = forms.CharField(
        label='Descripción',
        widget=forms.Textarea(attrs={'rows': 5})
    )

    def __init__(self, *args, **kwargs):
        pedidos_queryset = kwargs.pop('pedidos_queryset', Pedido.objects.none())
        super().__init__(*args, **kwargs)
        self.fields['pedido'].queryset = pedidos_queryset


class ActualizarTicketAdminForm(forms.Form):
    """
    Formulario para que el administrador responda y actualice un ticket.
    """

    estado = forms.ChoiceField(
        label='Estado',
        choices=TicketSoporte.ESTADOS
    )

    prioridad = forms.ChoiceField(
        label='Prioridad',
        choices=TicketSoporte.PRIORIDADES
    )

    respuesta = forms.CharField(
        label='Respuesta del administrador',
        required=False,
        widget=forms.Textarea(attrs={'rows': 5})
    )