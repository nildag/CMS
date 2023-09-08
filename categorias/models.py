from django.db import models


class Categoria(models.Model):
    """
    Esta clase representa una categoria dentro del sistema.
    Atributos:
    - nombre: Nombre representativo del rol. Ejemplo: Autor (str)
    - descripcion: Descripcion de lo que representa el rol. Ejemplo: Rol que se encargara de la creacion de contenidos dentro del sistema (str)
    - permisos: Atributo correspondiente a los permisos que posee el rol ( diccionario {str:Boolean} )
    """

    nombre = models.CharField(max_length=30, unique=True)
    descripcion = models.CharField(max_length=100)

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

        categoria = Categoria(nombre=nombre, descripcion=descripcion)
        categoria.save()
        return categoria

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
        verbose_name = "Categorias"
        verbose_name_plural = "Categorias"
        db_table = "categporia"
