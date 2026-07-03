"""
Archivo: models.py
Aplicación: accounts
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripción: Define los modelos de usuarios, clientes y empleados del sistema.
"""

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models


class PerfilUsuario(models.Model):
    """
    Modelo que permite asignar un rol a cada usuario del sistema.
    """

    ROL_CLIENTE = 'CLIENTE'
    ROL_ADMIN = 'ADMIN'
    ROL_REPARTIDOR = 'REPARTIDOR'
    ROL_SOPORTE = 'SOPORTE'

    ROLES = [
        (ROL_CLIENTE, 'Cliente'),
        (ROL_ADMIN, 'Administrador'),
        (ROL_REPARTIDOR, 'Repartidor'),
        (ROL_SOPORTE, 'Soporte Técnico'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=20, choices=ROLES, default=ROL_CLIENTE)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuario'

    def __str__(self):
        return f'{self.user.username} - {self.rol}'


class Cliente(models.Model):
    """
    Modelo que almacena los datos personales del cliente registrado.
    """

    dni_validator = RegexValidator(
        regex=r'^\d{8}$',
        message='El DNI debe contener exactamente 8 dígitos.'
    )

    telefono_validator = RegexValidator(
        regex=r'^\d{9}$',
        message='El teléfono debe contener exactamente 9 dígitos.'
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cliente')
    dni = models.CharField(max_length=8, unique=True, validators=[dni_validator])
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=9, validators=[telefono_validator])
    direccion = models.CharField(max_length=200)
    distrito = models.CharField(max_length=100)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['apellidos', 'nombres']

    def __str__(self):
        return f'{self.nombres} {self.apellidos}'


class Empleado(models.Model):
    """
    Modelo que almacena los datos de trabajadores administrativos o internos.
    """

    CARGO_ADMIN = 'ADMIN'
    CARGO_SUPERVISOR = 'SUPERVISOR'
    CARGO_ALMACEN = 'ALMACEN'
    CARGO_SOPORTE = 'SOPORTE'
    CARGO_CAJERO = 'CAJERO'

    CARGOS = [
        (CARGO_ADMIN, 'Administrador del Minimarket'),
        (CARGO_SUPERVISOR, 'Supervisor de Ventas'),
        (CARGO_ALMACEN, 'Encargado de Almacén'),
        (CARGO_SOPORTE, 'Soporte Técnico'),
        (CARGO_CAJERO, 'Cajero / Atención al Cliente'),
    ]

    dni_validator = RegexValidator(
        regex=r'^\d{8}$',
        message='El DNI debe contener exactamente 8 dígitos.'
    )

    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='empleado'
    )
    dni = models.CharField(max_length=8, unique=True, validators=[dni_validator])
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    cargo = models.CharField(max_length=30, choices=CARGOS)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        ordering = ['apellidos', 'nombres']

    def __str__(self):
        return f'{self.nombres} {self.apellidos} - {self.get_cargo_display()}'