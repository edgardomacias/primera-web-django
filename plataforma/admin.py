from django.contrib import admin
from .models import Restaurante, Resena, Usuario


@admin.register(Restaurante)
class RestauranteAdmin(admin.ModelAdmin):
    list_display = ["nombre", "ciudad", "tipo_cocina", "telefono"]
    search_fields = ["nombre", "ciudad", "tipo_cocina"]


@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    list_display = ["restaurante", "calificacion", "fecha"]
    list_filter = ["calificacion"]


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ["nombre", "email", "fecha_registro"]
    search_fields = ["nombre", "email"]
