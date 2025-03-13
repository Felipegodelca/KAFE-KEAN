# Generated by Django 4.2.17 on 2025-01-23 15:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Perfil",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "foto_perfil",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="imagenes_perfiles/",
                        verbose_name="Foto de Perfil",
                    ),
                ),
                (
                    "preferencias",
                    models.TextField(
                        blank=True, null=True, verbose_name="Preferencias"
                    ),
                ),
                (
                    "biografia",
                    models.TextField(blank=True, null=True, verbose_name="Biografía"),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Articulo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "titulo",
                    models.CharField(
                        help_text="Introduce un título descriptivo para el artículo (máximo 200 caracteres).",
                        max_length=200,
                        verbose_name="Título",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        blank=True,
                        help_text="URL amigable para este artículo.",
                        max_length=200,
                        null=True,
                        verbose_name="Slug",
                    ),
                ),
                (
                    "contenido",
                    models.TextField(
                        help_text="Escribe el contenido completo del artículo aquí.",
                        verbose_name="Contenido",
                    ),
                ),
                (
                    "fecha_publicacion",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Fecha de publicación"
                    ),
                ),
                (
                    "tema",
                    models.CharField(
                        choices=[
                            ("FIL", "Filosofía"),
                            ("PSI", "Psicología"),
                            ("NEG", "Negocios"),
                        ],
                        default="FIL",
                        max_length=3,
                        verbose_name="Tema",
                    ),
                ),
                (
                    "etiquetas",
                    models.CharField(
                        blank=True,
                        help_text="Etiquetas separadas por comas, ej: reflexión, conciencia.",
                        max_length=200,
                        null=True,
                        verbose_name="Etiquetas",
                    ),
                ),
                (
                    "imagen",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="imagenes_articulos/",
                        verbose_name="Imagen",
                    ),
                ),
                (
                    "autor",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Artículo",
                "verbose_name_plural": "Artículos",
                "ordering": ["-fecha_publicacion"],
            },
        ),
    ]
