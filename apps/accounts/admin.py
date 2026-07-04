"""
Archivo: admin.py
Aplicación: accounts
Proyecto: Sistema Web Tiendas Mass
Autor: Daniel Medina
Descripción: Configura la administración de perfiles, clientes y empleados.
"""

from django.contrib import admin
from .models import PerfilUsuario, Cliente, Empleado


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'rol', 'telefono', 'activo', 'fecha_creacion')
    list_filter = ('rol', 'activo')
    search_fields = ('user__username', 'user__email', 'telefono')


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('dni', 'nombres', 'apellidos', 'email', 'telefono', 'distrito', 'activo')
    list_filter = ('distrito', 'activo')
    search_fields = ('dni', 'nombres', 'apellidos', 'email')


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('dni', 'nombres', 'apellidos', 'cargo', 'email', 'telefono', 'activo')
    list_filter = ('cargo', 'activo')
    search_fields = ('dni', 'nombres', 'apellidos', 'email')