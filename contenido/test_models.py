from django.test import TestCase
from usuario.models import User  # Importa el modelo de usuario personalizado
from .models import Contenido, Categoria

class ContenidoModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='12345')  # Usa el modelo de usuario personalizado
        categoria = Categoria.objects.create(nombre='test categoria')
        Contenido.objects.create(titulo='test titulo', cuerpo='test cuerpo', autor=user, categoria=categoria)


    def test_titulo_label(self):
        contenido = Contenido.objects.get(id=1)
        field_label = contenido._meta.get_field('titulo').verbose_name
        self.assertEquals(field_label, 'titulo')

    def test_cuerpo_label(self):
        contenido = Contenido.objects.get(id=1)
        field_label = contenido._meta.get_field('cuerpo').verbose_name
        self.assertEquals(field_label, 'cuerpo')

    def test_autor_label(self):
        contenido = Contenido.objects.get(id=1)
        field_label = contenido._meta.get_field('autor').verbose_name
        self.assertEquals(field_label, 'autor')

    def test_categoria_label(self):
        contenido = Contenido.objects.get(id=1)
        field_label = contenido._meta.get_field('categoria').verbose_name
        self.assertEquals(field_label, 'categoria')

    def test_fecha_creacion_label(self):
        contenido = Contenido.objects.get(id=1)
        field_label = contenido._meta.get_field('fecha_creacion').verbose_name
        self.assertEquals(field_label, 'fecha creacion')

    def test_titulo_max_length(self):
        contenido = Contenido.objects.get(id=1)
        max_length = contenido._meta.get_field('titulo').max_length
        self.assertEquals(max_length, 30)

    def test_object_name_is_title_and_author(self):
        contenido = Contenido.objects.get(id=1)
        expected_object_name = f'{contenido.titulo} - {contenido.autor.first_name} {contenido.autor.last_name}'
        self.assertEquals(expected_object_name, str(contenido))