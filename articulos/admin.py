from django.contrib import admin
from .models import Articulo
from django.utils.translation import gettext_lazy as _

@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    """
    Configuración personalizada para la administración del modelo Articulo.
    """
    # Campos visibles en la lista de artículos
    list_display = ('titulo', 'get_tema_display', 'fecha_publicacion', 'autor')
    list_display_links = ('titulo',)  # El título será clickeable
    ordering = ('-fecha_publicacion',)  # Orden descendente por fecha de publicación

    # Campos por los que se puede buscar
    search_fields = ('titulo', 'contenido', 'etiquetas')

    # Filtros laterales
    list_filter = ('tema', 'fecha_publicacion', 'autor')

    # Configuración de los grupos de campos
    fieldsets = (
        (_("Información del Artículo"), {
            'fields': ('titulo', 'contenido', 'tema', 'etiquetas', 'imagen', 'autor'),
        }),
        (_("Fechas"), {
            'fields': ('fecha_publicacion',),
        }),
    )

    # Campos de solo lectura
    readonly_fields = ('fecha_publicacion',)

    # Configuración de acciones personalizadas
    actions = ['marcar_como_filosofia', 'marcar_como_psicologia', 'marcar_como_negocios']

    # Definición de acciones
    def marcar_como_filosofia(self, request, queryset):
        """
        Marca los artículos seleccionados como Filosofía.
        """
        updated = queryset.update(tema='FIL')
        self.message_user(request, _("%d artículo(s) marcado(s) como Filosofía.") % updated)
    marcar_como_filosofia.short_description = _("Marcar como Filosofía")

    def marcar_como_psicologia(self, request, queryset):
        """
        Marca los artículos seleccionados como Psicología.
        """
        updated = queryset.update(tema='PSI')
        self.message_user(request, _("%d artículo(s) marcado(s) como Psicología.") % updated)
    marcar_como_psicologia.short_description = _("Marcar como Psicología")

    def marcar_como_negocios(self, request, queryset):
        """
        Marca los artículos seleccionados como Negocios.
        """
        updated = queryset.update(tema='NEG')
        self.message_user(request, _("%d artículo(s) marcado(s) como Negocios.") % updated)
    marcar_como_negocios.short_description = _("Marcar como Negocios")