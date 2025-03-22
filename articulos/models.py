from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils.text import slugify
#from PIL import Image  # Para validar imágenes


class Articulo(models.Model):
    # Opciones para el campo de tema
    TEMA_OPCIONES = [
        ('FIL', _('Filosofía')),
        ('PSI', _('Psicología')),
        ('NEG', _('Negocios')),
    ]

    # Campos del modelo
    titulo = models.CharField(
        max_length=200,
        verbose_name=_("Título"),
        help_text=_("Introduce un título descriptivo para el artículo (máximo 200 caracteres)."),
    )
    slug = models.SlugField(
    max_length=200,
    blank=True,
    null=True,  # Permite valores NULL temporalmente
    verbose_name=_("Slug"),
    help_text=_("URL amigable para este artículo."),
    )
    contenido = models.TextField(
        verbose_name=_("Contenido"),
        help_text=_("Escribe el contenido completo del artículo aquí."),
    )
    fecha_publicacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Fecha de publicación"),
    )
    tema = models.CharField(
        max_length=3,
        choices=TEMA_OPCIONES,
        default='FIL',
        verbose_name=_("Tema"),
    )
    etiquetas = models.CharField(
        max_length=200,
        help_text=_("Etiquetas separadas por comas, ej: reflexión, conciencia."),
        blank=True,
        null=True,
        verbose_name=_("Etiquetas"),
    )
    imagen = models.ImageField(
        upload_to='imagenes_articulos/',
        blank=True,
        null=True,
        verbose_name=_("Imagen"),
    )
    autor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    # Métodos adicionales
    def clean(self):
        """
        Validación personalizada para asegurar la calidad de los datos.
        """
        if len(self.titulo) < 5:
            raise ValidationError(_('El título debe tener al menos 5 caracteres.'))
        if self.etiquetas and len(self.etiquetas.split(',')) > 10:
            raise ValidationError(_('No puedes agregar más de 10 etiquetas.'))

    #   if self.imagen:
    #       try:
    #           img = Image.open(self.imagen)
    #           if img.format.lower() not in ['jpeg', 'png']:
    #               raise ValidationError(_('Solo se permiten imágenes JPEG o PNG.'))
    #           if self.imagen.size > 5 * 1024 * 1024:
    #               raise ValidationError(_('El tamaño de la imagen no puede exceder los 5MB.'))
    #       except Exception:
    #          raise ValidationError(_('La imagen proporcionada no es válida.'))

    def save(self, *args, **kwargs):
        """
        Generar automáticamente el slug basado en el título.
        Si ya existe un slug igual, se añade un sufijo numérico.
        """
        if not self.slug:
            base_slug = slugify(self.titulo)
            unique_slug = base_slug
            counter = 1
            while Articulo.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    # Configuración de metadatos
    class Meta:
        verbose_name = _("Artículo")
        verbose_name_plural = _("Artículos")
        ordering = ['-fecha_publicacion']

    # Representación en texto
    def __str__(self):
        return self.titulo

    def etiquetas_como_lista(self):
        """
        Devuelve las etiquetas como una lista de strings.
        """
        return [etiqueta.strip() for etiqueta in self.etiquetas.split(',')] if self.etiquetas else []


class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    foto_perfil = models.ImageField(
        upload_to='imagenes_perfiles/',
        blank=True,
        null=True,
        verbose_name=_("Foto de Perfil"),
    )
    preferencias = models.TextField(blank=True, null=True, verbose_name=_("Preferencias"))
    biografia = models.TextField(blank=True, null=True, verbose_name=_("Biografía"))

    def __str__(self):
        return f"Perfil de {self.user.username}"

    def clean(self):
        """
        Validación personalizada para la biografía y preferencias.
        """
        if self.preferencias and len(self.preferencias.split(',')) > 20:
            raise ValidationError(_('No puedes agregar más de 20 preferencias.'))