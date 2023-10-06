
from django.db import models

class Permiso(models.Model):

    """
    Esta clase representa a un permiso dentro del sistema.
    Atributos:
    - nombre: Contiene todos los permisos del sistema en un formato { <nombre-permiso> : <activo o desactivado> } (diccionario {str:Boolean})
    """

    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Permiso"
        verbose_name_plural = "Permisos"
        db_table = "permiso"

    def __str__(self):

        """
        Este metodo retorna el nombre del permiso.
        :return: Se retorna un str
        """

        return f"{self.nombre}"
    
    @classmethod
    def crear(cls, nombre):

        """
        Este metodo sirve para crear un permiso
        :nombre: Nombre del permiso a crear (str)
        :return: Retorna un Permiso
        """

        permiso = Permiso(nombre=nombre)
        permiso.save()
        return permiso
    
    @classmethod
    def getAll(cls):

        """
        Este metodo retorna todos los permisos del sistema
        :return: Retorna una lista de permisos
        """

        return Permiso.objects.all()
    
    def getByNombre(nombre):

        """
        Este metodo retorna un permiso por su nombre
        :nombre: Nombre del permiso a buscar (str)
        :return: Retorna un Permiso
        """

        return Permiso.objects.get(nombre=nombre)
    
"""
'Visualizar contenido': False,
'Crear contenido' : False,
'Editar contenido' : False,
'Publicar contenido' : False,
'Eliminar contenido': False,
'Puntuar contenido': False,
'Visualizar historial del contenido': False,
'Administrar roles': False,
'Administrar categorias': False,
"""