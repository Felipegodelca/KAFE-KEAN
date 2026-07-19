from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Articulo(models.Model):
    titulo = models.CharField(_("título"), max_length=200)
    slug = models.SlugField(_("slug"), max_length=220, unique=True, blank=True)
    descripcion = models.TextField(_("descripción"))
    contenido = models.TextField(_("contenido"), blank=True)
    imagen = models.ImageField(_("imagen"), upload_to="articulos/", blank=True, null=True)
    fecha_publicacion = models.DateTimeField(_("fecha de publicación"), auto_now_add=True)
    actualizado = models.DateTimeField(_("actualizado"), auto_now=True)

    class Meta:
        ordering = ["-fecha_publicacion"]
        verbose_name = _("artículo")
        verbose_name_plural = _("artículos")

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.titulo) or "articulo"
            candidate = base_slug
            counter = 2
            while Articulo.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                candidate = f"{base_slug}-{counter}"
                counter += 1
            self.slug = candidate
        super().save(*args, **kwargs)
