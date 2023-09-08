from django.db import models
from permisos.models import Permisos

class Rol(models.Model):

    """
    Esta clase representa un Rol dentro del sistema.
    Atributos:
    - nombre: Nombre representativo del rol. Ejemplo: Autor (str)
    - descripcion: Descripcion de lo que representa el rol. Ejemplo: Rol que se encargara de la creacion de contenidos dentro del sistema (str)
    - permisos: Atributo correspondiente a los permisos que posee el rol ( diccionario {str:Boolean} )
    """

    nombre = models.CharField(max_length=30, unique=True)
    descripcion = models.CharField(max_length=100)
    permisos = models.JSONField()

    def __str__(self):

        """
        Este metodo retorna el nombre y la descripcion del rol.
        :return: Se retorna un str
        """

        return f"{self.nombre} : {self.descripcion}"

    @classmethod
    def crear(cls, nombre, descripcion):

        """
        Este metodo sirve para crear un rol
        :nombre: Nombre del rol a crear (str)
        :descripcion: Descripcion del rol a crear (str)
        :permisos: Los permisos que se le asignaran al nuevo rol creado (diccionario)
        :return: Retorna un Rol con los permisos predefinidos
        """

        permisos_predeterminados = Permisos().permisos
        rol = Rol(nombre=nombre, descripcion=descripcion, permisos=permisos_predeterminados)
        rol.save()
        return rol

    def eliminar(self):

        """
        Metodo que elimina el rol correspondiente a la instancia actual
        """

        self.delete()

    @classmethod
    def eliminar_por_nombre(cls, nombre):

        """
        Esta funcion elimina un rol por el nombre que es recibido como parametro
        :nombre: Nombre del rol (str)
        """

        cls.objects.filter(nombre=nombre).delete()

    def cambiar_permisos(self, permisos):

        """
        Este metodo permite cambiar los permisos del rol actual
        :permisos: Recibe la plantilla de permisos que va a tener ahora el rol (Permisos)
        """

        self.permisos = permisos
        self.save()

    @classmethod
    def obtener_por_nombre(cls, nombre):

        """
        Obtenemos un rol por el nombre
        :nombre: El nombre por el cual buscaremos el rol (str)
        :return: (Rol)
        """
        
        try:
            return cls.objects.get(nombre=nombre)
        except cls.DoesNotExist:
            return None

    @classmethod
    def obtener_todos(cls):

        """
        Obtenemos todos los Roles
        :return: (Rol-list)
        """

        return cls.objects.all()

    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"
        db_table = "rol"
