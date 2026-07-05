"""
Archivo: forms.py
Aplicación: payments
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripción: Define formularios para procesar pagos simulados según el método seleccionado.
"""

from datetime import date

from django import forms

from .models import Pago, Venta


class PagoSimuladoForm(forms.Form):
    """
    Formulario para simular pagos con Yape, Plin, tarjeta, transferencia o contra entrega.
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

    banco = forms.CharField(
        label='Banco',
        max_length=50,
        required=False
    )

    tarjeta_titular = forms.CharField(
        label='Titular de la tarjeta',
        max_length=100,
        required=False
    )

    tarjeta_numero = forms.CharField(
        label='Número de tarjeta',
        max_length=19,
        required=False
    )

    tarjeta_mes = forms.IntegerField(
        label='Mes de vencimiento',
        min_value=1,
        max_value=12,
        required=False
    )

    tarjeta_anio = forms.IntegerField(
        label='Año de vencimiento',
        min_value=date.today().year,
        max_value=2040,
        required=False
    )

    tarjeta_cvv = forms.CharField(
        label='CVV',
        max_length=4,
        required=False,
        widget=forms.PasswordInput
    )

    observacion = forms.CharField(
        label='Observación',
        required=False,
        widget=forms.Textarea(attrs={'rows': 3})
    )

    def clean_tarjeta_numero(self):
        """
        Valida que el número de tarjeta tenga solo dígitos y una longitud aceptable.
        """
        numero = self.cleaned_data.get('tarjeta_numero', '')
        numero = numero.replace(' ', '').replace('-', '')

        if numero and (not numero.isdigit() or len(numero) not in range(13, 20)):
            raise forms.ValidationError('El número de tarjeta debe tener entre 13 y 19 dígitos.')

        return numero

    def clean_tarjeta_cvv(self):
        """
        Valida el CVV sin almacenarlo posteriormente.
        """
        cvv = self.cleaned_data.get('tarjeta_cvv', '')

        if cvv and (not cvv.isdigit() or len(cvv) not in [3, 4]):
            raise forms.ValidationError('El CVV debe tener 3 o 4 dígitos.')

        return cvv

    def clean(self):
        """
        Aplica validaciones según el método de pago seleccionado.
        """
        cleaned_data = super().clean()

        metodo_pago = cleaned_data.get('metodo_pago')
        numero_operacion = cleaned_data.get('numero_operacion')
        banco = cleaned_data.get('banco')

        tarjeta_titular = cleaned_data.get('tarjeta_titular')
        tarjeta_numero = cleaned_data.get('tarjeta_numero')
        tarjeta_mes = cleaned_data.get('tarjeta_mes')
        tarjeta_anio = cleaned_data.get('tarjeta_anio')
        tarjeta_cvv = cleaned_data.get('tarjeta_cvv')

        if metodo_pago in [Pago.METODO_YAPE, Pago.METODO_PLIN]:
            if not numero_operacion:
                self.add_error(
                    'numero_operacion',
                    'Debes ingresar el número de operación de la billetera digital.'
                )

        if metodo_pago == Pago.METODO_TRANSFERENCIA:
            if not banco:
                self.add_error('banco', 'Debes ingresar el banco de la transferencia.')

            if not numero_operacion:
                self.add_error(
                    'numero_operacion',
                    'Debes ingresar el número de operación de la transferencia.'
                )

        if metodo_pago == Pago.METODO_TARJETA:
            if not tarjeta_titular:
                self.add_error('tarjeta_titular', 'Debes ingresar el titular de la tarjeta.')

            if not tarjeta_numero:
                self.add_error('tarjeta_numero', 'Debes ingresar el número de tarjeta.')

            if not tarjeta_mes:
                self.add_error('tarjeta_mes', 'Debes ingresar el mes de vencimiento.')

            if not tarjeta_anio:
                self.add_error('tarjeta_anio', 'Debes ingresar el año de vencimiento.')

            if not tarjeta_cvv:
                self.add_error('tarjeta_cvv', 'Debes ingresar el CVV.')

            if tarjeta_mes and tarjeta_anio:
                hoy = date.today()

                if tarjeta_anio < hoy.year or (tarjeta_anio == hoy.year and tarjeta_mes < hoy.month):
                    self.add_error('tarjeta_mes', 'La tarjeta está vencida.')

        return cleaned_data

    def obtener_marca_tarjeta(self):
        """
        Identifica una marca básica de tarjeta según el primer dígito.
        """
        numero = self.cleaned_data.get('tarjeta_numero', '')

        if numero.startswith('4'):
            return 'Visa'

        if numero.startswith('5'):
            return 'Mastercard'

        return 'Tarjeta'