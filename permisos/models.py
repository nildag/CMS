from django.db import models

class Permisos():

    """
    Esta clase representa a todos los permisos del sistema como un template
    Atributos:
    - permisos: Contiene todos los permisos del sistema en un formato { <nombre-permiso> : <activo o desactivado> } (diccionario {str:Boolean})
    """

    permisos = {}

    def __init__(self):
        self.permisos = {
            'Visualizar contenido': False,
            'Crear contenido' : False,
            'Editar contenido' : False,
            'Publicar contenido' : False,
            'Eliminar contenido': False,
            'Puntuar contenido': False,
            'Visualizar historial del contenido': False,
            'Administrar roles': False,
            'Administrar categorias': False,
        }
