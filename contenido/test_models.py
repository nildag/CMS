from django.test import TestCase
from usuario.models import User  # Importa el modelo de usuario personalizado
from .models import Contenido, Categoria

class ContenidoModelTest(TestCase):
    """
    Esta clase contiene pruebas para el modelo de Contenido.

    Métodos de Clase:
        setUpTestData(): Configura los datos de prueba.

    Métodos de Prueba:
        test_titulo_label(): Prueba la etiqueta del campo 'titulo'.
        test_cuerpo_label(): Prueba la etiqueta del campo 'cuerpo'.
        test_autor_label(): Prueba la etiqueta del campo 'autor'.
        test_categoria_label(): Prueba la etiqueta del campo 'categoria'.
        test_fecha_creacion_label(): Prueba la etiqueta del campo 'fecha_creacion'.
        test_titulo_max_length(): Prueba la longitud máxima del campo 'titulo'.
        test_object_name_is_title_and_author(): Prueba el nombre del objeto Contenido.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Configura los datos de prueba.
        """
        user = User.objects.create_user(username='testuser', password='12345')  # Usa el modelo de usuario personalizado
        categoria = Categoria.objects.create(nombre='test categoria')
        Contenido.objects.create(titulo='test titulo', cuerpo='test cuerpo', autor=user, categoria=categoria)

    def test_titulo_label(self):
        """
        Prueba la etiqueta del campo 'titulo'.
        """
        contenido = Contenido.objects.get(id=1)
        field_label = contenido._meta.get_field('titulo').verbose_name
        self.assertEquals(field_label, 'titulo')

    def test_cuerpo_label(self):
        """
        Prueba la etiqueta del campo 'cuerpo'.
        """
        contenido = Contenido.objects.get(id=1)
        field_label = contenido._meta.get_field('cuerpo').verbose_name
        self.assertEquals(field_label, 'cuerpo')

    def test_autor_label(self):
        """
        Prueba la etiqueta del campo 'autor'.
        """
        contenido = Contenido.objects.get(id=1)
        field_label = contenido._meta.get_field('autor').verbose_name
        self.assertEquals(field_label, 'autor')

    def test_categoria_label(self):
        """
        Prueba la etiqueta del campo 'categoria'.
        """
        contenido = Contenido.objects.get(id=1)
        field_label = contenido._meta.get_field('categoria').verbose_name
        self.assertEquals(field_label, 'categoria')

    def test_fecha_creacion_label(self):
        """
        Prueba la etiqueta del campo 'fecha_creacion'.
        """
        contenido = Contenido.objects.get(id=1)
        field_label = contenido._meta.get_field('fecha_creacion').verbose_name
        self.assertEquals(field_label, 'fecha creacion')

    def test_titulo_max_length(self):
        """
        Prueba la longitud máxima del campo 'titulo'.
        """
        contenido = Contenido.objects.get(id=1)
        max_length = contenido._meta.get_field('titulo').max_length
        self.assertEquals(max_length, 200)

    def test_object_name_is_title_and_author(self):
        """
        Prueba el nombre del objeto Contenido.
        """
        contenido = Contenido.objects.get(id=1)
        expected_object_name = f'{contenido.titulo} - {contenido.autor.first_name} {contenido.autor.last_name}'
        self.assertEquals(expected_object_name, str(contenido))
