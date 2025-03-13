from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from .models import Articulo
from django.utils.translation import activate
from django.contrib.auth.models import User


class ArticuloTests(TestCase):
    def setUp(self):
        # Activa el idioma predeterminado para las pruebas
        activate('es')

        # Crea un usuario de prueba
        self.user = User.objects.create_user(username='testuser', password='12345')

        # Crea un artículo de prueba
        self.articulo = Articulo.objects.create(
            titulo="Artículo de Prueba",
            contenido="Contenido de prueba para el artículo.",
            tema="FIL",
            etiquetas="prueba,artículo",
            autor=self.user
        )

    def test_lista_articulos_view(self):
        response = self.client.get(reverse('articulos:lista_articulos'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articulos/lista_articulos.html')
        self.assertContains(response, self.articulo.titulo)

    def test_detalle_articulo_view(self):
        response = self.client.get(reverse('articulos:detalle_articulo', args=[self.articulo.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articulos/detalle_articulo.html')
        self.assertContains(response, self.articulo.contenido)

    def test_crear_articulo_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('articulos:crear_articulo'), {
            'titulo': 'Nuevo Artículo',
            'contenido': 'Contenido del nuevo artículo.',
            'tema': 'PSI',
            'etiquetas': 'nuevo,artículo',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Articulo.objects.filter(titulo='Nuevo Artículo').exists())

    def test_editar_articulo_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('articulos:editar_articulo', args=[self.articulo.id]), {
            'titulo': 'Artículo Editado',
            'contenido': 'Contenido editado.',
            'tema': 'NEG',
            'etiquetas': 'editado',
        })
        self.assertEqual(response.status_code, 302)
        self.articulo.refresh_from_db()
        self.assertEqual(self.articulo.titulo, 'Artículo Editado')

    def test_eliminar_articulo_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('articulos:eliminar_articulo', args=[self.articulo.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Articulo.objects.filter(id=self.articulo.id).exists())

    def test_obtener_tipo_cambio_mock(self):
        # Mockea la respuesta de la API para evitar dependencias externas
        with patch('articulos.views.requests.get') as mocked_get:
            mocked_get.return_value.status_code = 200
            mocked_get.return_value.json.return_value = {
                'result': 'success',
                'conversion_rates': {'MXN': 19.5, 'BRL': 4.5, 'CAD': 1.3}
            }
            from articulos.views import obtener_tipo_cambio
            resultado = obtener_tipo_cambio()
            self.assertTrue(len(resultado['tipos_de_cambio']) > 0)

    def test_unauthorized_access(self):
        # Comprueba el acceso no autorizado
        for view_name, args in [('articulos:crear_articulo', []), 
                                ('articulos:editar_articulo', [self.articulo.id]), 
                                ('articulos:eliminar_articulo', [self.articulo.id])]:
            response = self.client.get(reverse(view_name, args=args))
            self.assertRedirects(response, f"{reverse('articulos:login')}?next={reverse(view_name, args=args)}")