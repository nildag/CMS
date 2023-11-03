from django.test import TestCase
from .models import tipoContenido

class TipoContenidoTestCase(TestCase):

    def setUp(self):
        self.tipo1 = tipoContenido.crear(nombre='Wiki', descripcion='Contenido del tipo Wiki')
        self.tipo2 = tipoContenido.crear(nombre='Blog', descripcion='Contenido del tipo Blog')

    def test_crear_tipo_contenido(self):
        self.assertEqual(self.tipo1.nombre, 'Wiki')
        self.assertEqual(self.tipo2.nombre, 'Blog')
        self.assertEqual(self.tipo1.descripcion, 'Contenido del tipo Wiki')
        self.assertEqual(self.tipo2.descripcion, 'Contenido del tipo Blog')

    def test_eliminar_tipo_contenido(self):
        self.tipo1.eliminar()
        self.assertIsNone(tipoContenido.obtener_por_nombre('Wiki'))

    def test_eliminar_por_nombre(self):
        tipoContenido.eliminar_por_nombre('Wiki')
        self.assertIsNone(tipoContenido.obtener_por_nombre('Wiki'))

    def test_obtener_por_nombre(self):
        tipo = tipoContenido.obtener_por_nombre('Wiki')
        self.assertEqual(tipo, self.tipo1)

    def test_obtener_todos(self):
        tipos = tipoContenido.obtener_todos()
        self.assertIn(self.tipo1, tipos)
        self.assertIn(self.tipo2, tipos)

    def test_get_by_id(self):
        tipo = tipoContenido.getById(self.tipo1.id)
        self.assertEqual(tipo, self.tipo1)

    def test_nombre_unico(self):
        with self.assertRaises(Exception):
            tipoContenido.crear(nombre='Wiki', descripcion='Otra descripción')

    def test_obtener_por_nombre_inexistente(self):
        tipo = tipoContenido.obtener_por_nombre('TipoInexistente')
        self.assertIsNone(tipo)
