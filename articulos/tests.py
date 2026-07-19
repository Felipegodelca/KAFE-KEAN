from django.test import TestCase
from django.urls import reverse

from .models import Articulo


class ArticulosSmokeTests(TestCase):
    def test_homepage_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_article_slug_detail_loads(self):
        articulo = Articulo.objects.create(titulo="Prueba KAFE", descripcion="Demo")
        response = self.client.get(reverse("articulos:detalle_articulo", args=[articulo.slug]))
        self.assertEqual(response.status_code, 200)
