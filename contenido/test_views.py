from django.test import TestCase, Client
from django.urls import reverse
from usuario.models import User  
from contenido.models import Contenido, Categoria
from usuario.models import UserCategoria
from contenido.forms import ContenidoForm


class EditarContenidoViewTest(TestCase):
    """
    Esta clase contiene pruebas para la vista de edición de contenido.

    Atributos de Clase:
        user (User): Un usuario de prueba para realizar las pruebas.
        categoria (Categoria): Una categoría de prueba para el contenido.
        contenido (Contenido): Un contenido de prueba para las pruebas.

    Métodos de Clase:
        setUpTestData(): Configura los datos de prueba.
        setUp(): Configura el entorno de prueba.

    Métodos de Prueba:
        test_editar_contenido_view_GET(): Prueba la solicitud GET a la vista de edición.
        test_editar_contenido_view_POST_valid(): Prueba la solicitud POST con datos válidos.
        test_editar_contenido_view_POST_invalid(): Prueba la solicitud POST con datos no válidos.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Configura los datos de prueba.
        """
        # Crear un usuario usando el modelo de usuario personalizado
        cls.user = User.objects.create_user(username='testuser', password='12345')
        # Crear una categoría
        cls.categoria = Categoria.objects.create(nombre='test categoria')
        # Crear un contenido
        cls.contenido = Contenido.objects.create(titulo='test titulo', cuerpo='test cuerpo', autor=cls.user, categoria=cls.categoria)

    def setUp(self):
        """
        Configura el entorno de prueba.
        """
        self.client = Client()
        self.client.login(username='testuser', password='12345')

    def test_editar_contenido_view_GET(self):
        """
        Prueba la solicitud GET a la vista de edición.
        """
        # Emitir una solicitud GET a la vista
        response = self.client.get(reverse('contenido:editar_contenido', args=[self.contenido.id]))

    def test_editar_contenido_view_POST_valid(self):
        """
        Prueba la solicitud POST con datos válidos.
        """
        # Emitir una solicitud POST a la vista con datos válidos
        response = self.client.post(reverse('contenido:editar_contenido', args=[self.contenido.id]), {
            'titulo': 'test titulo editado',
            'cuerpo': 'test cuerpo editado',
            'categoria': self.categoria.id
        })

    def test_editar_contenido_view_POST_invalid(self):
        """
        Prueba la solicitud POST con datos no válidos.
        """
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
