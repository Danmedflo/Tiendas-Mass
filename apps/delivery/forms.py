"""
Archivo: forms.py
Aplicación: delivery
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripción: Define formularios para actualizar el estado de las entregas.
"""

from django import forms

from .models import Entrega


class ActualizarEntregaForm(forms.Form):
    """
    Formulario usado por el repartidor para actualizar el estado de una entrega.
    """

    estado = forms.ChoiceField(
        label='Estado de entrega',
        choices=[
            (Entrega.ESTADO_EN_CAMINO, 'En camino'),
            (Entrega.ESTADO_ENTREGADA, 'Entregada'),
            (Entrega.ESTADO_FALLIDA, 'Fallida'),
            (Entrega.ESTADO_REPROGRAMADA, 'Reprogramada'),
        ]
    )

    observacion = forms.CharField(
        label='Observación',
        required=False,
        widget=forms.Textarea(attrs={'rows': 3})
    )