from django.db import models


class Categoria(models.Model):
    """
    Esta clase representa una categoría dentro del sistema.

    Atributos:
    - nombre (str): Nombre representativo de la categoría.
    - descripcion (str): Descripción de la categoría.

    Ejemplo:
    nombre: "Machine Learning"
    descripcion: "Artículos de machine learning"
    """

    nombre = models.CharField(max_length=30, unique=True)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        """
        Este método retorna el nombre y la descripción de la categoría.

        Returns:
        str: Nombre y descripción de la categoría.
        """
        return f"{self.nombre} : {self.descripcion}"

    @classmethod
    def crear(cls, nombre, descripcion):
        """
        Este método sirve para crear una categoría.

        Args:
        nombre (str): Nombre de la categoría a crear.
        descripcion (str): Descripción de la categoría a crear.

        Returns:
        Categoria: La categoría creada.
        """
        categoria = Categoria(nombre=nombre, descripcion=descripcion)
        categoria.save()
        return categoria

    def eliminar(self):
        """
        Método que elimina la categoría correspondiente a la instancia actual.
        """
        self.delete()

    @classmethod
    def eliminar_por_nombre(cls, nombre):
        """
        Esta función elimina una categoría por el nombre que es recibido como parámetro.

        Args:
        nombre (str): Nombre de la categoría a eliminar.
        """
        cls.objects.filter(nombre=nombre).delete()

    @classmethod
    def obtener_por_nombre(cls, nombre):
        """
        Obtenemos una categoría por el nombre.

        Args:
        nombre (str): El nombre por el cual buscaremos la categoría.

        Returns:
        Categoria: La categoría encontrada, o None si no existe.
        """
        try:
            return cls.objects.get(nombre=nombre)
        except cls.DoesNotExist:
            return None

    @classmethod
    def obtener_todos(cls):
        """
        Obtenemos todas las categorías.

        Returns:
        list: Lista de todas las categorías.
        """
        return cls.objects.all()
    
    @classmethod
    def getById(cls, id):
            """
            Obtenemos una categoría por el id.

            Args:
            id (int): El id por el cual buscaremos la categoría.

            Returns:
            Categoria: La categoría encontrada.
            """
            return cls.objects.get(id=id)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        db_table = "categoria"
