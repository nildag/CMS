from django.test import TestCase, Client
from django.urls import reverse
from usuario.models import User  
from contenido.models import Contenido, Categoria
from usuario.models import UserCategoria
from contenido.forms import ContenidoForm


class EditarContenidoViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
# Crear un usuario usando el modelo de usuario personalizado
        cls.user = User.objects.create_user(username='testuser', password='12345')
       # Crear una categoría
        cls.categoria = Categoria.objects.create(nombre='test categoria')
       # Crear un contenido
        cls.contenido = Contenido.objects.create(titulo='test titulo', cuerpo='test cuerpo', autor=cls.user, categoria=cls.categoria)

    def setUp(self):

        self.client = Client()
        self.client.login(username='testuser', password='12345')

    def test_editar_contenido_view_GET(self):
        # Emitir una solicitud GET a la vista
        response = self.client.get(reverse('contenido:editar_contenido', args=[self.contenido.id]))


    def test_editar_contenido_view_POST_valid(self):
        # Emitir una solicitud POST a la vista con datos válidos
        response = self.client.post(reverse('contenido:editar_contenido', args=[self.contenido.id]), {
            'titulo': 'test titulo editado',
            'cuerpo': 'test cuerpo editado',
            'categoria': self.categoria.id
        })


    def test_editar_contenido_view_POST_invalid(self):
       # Emitir una solicitud POST a la vista con datos no válidos
        response = self.client.post(reverse('contenido:editar_contenido', args=[self.contenido.id]), {
            'titulo': '',
            'cuerpo': 'test cuerpo editado',
            'categoria': self.categoria.id
        })
       # Verifique que el código de estado de respuesta sea 200
        self.assertEqual(response.status_code, 200)
      # Comprobar que el formulario se muestra con errores
        self.assertIsInstance(response.context['form'], ContenidoForm)
        self.assertTrue(response.context['form'].errors)