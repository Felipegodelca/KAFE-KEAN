from django.contrib import admin

from .models import Articulo


@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    list_display = ("titulo", "fecha_publicacion", "actualizado")
    prepopulated_fields = {"slug": ("titulo",)}
    search_fields = ("titulo", "descripcion", "contenido")
