from django.db import models


class Categoria(models.Model):
    """
    Esta clase representa una categoria dentro del sistema.
    Atributos:
    - nombre: Nombre representativo de la categoria.
    - descripcion: Descripcion de la categoria.
    Ejemplo:    nombre: Machine Learning
                descripcion: Artiuclos de machine learning
    """

    nombre = models.CharField(max_length=30, unique=True)
    descripcion = models.CharField(max_length=100)

    def __str__(self):

        """
        Este metodo retorna el nombre y la descripcion de la categotia.
        :return: Se retorna un str
        """

        return f"{self.nombre} : {self.descripcion}"

    @classmethod
    def crear(cls, nombre, descripcion):

        """
        Este metodo sirve para crear una categoria
        :nombre: Nombre de la categoria a crear (str)
        :descripcion: Descripcion de la categoria a crear (str)
        :return: Retorna la categoria
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
        Esta funcion elimina una categoria por el nombre que es recibido como parametro
        :nombre: Nombre de la categoria (str)
        """

        cls.objects.filter(nombre=nombre).delete()

    @classmethod
    def obtener_por_nombre(cls, nombre):

        """
        Obtenemos una categoria por el nombre
        :nombre: El nombre por el cual buscaremos la categoria (str)
        :return: (Categoria)
        """

        try:
            return cls.objects.get(nombre=nombre)
        except cls.DoesNotExist:
            return None

    @classmethod
    def obtener_todos(cls):

        """
        Obtenemos todas las categorias
        :return: (Categorias-list)
        """

        return cls.objects.all()

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        db_table = "categoria"
