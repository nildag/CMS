from django.db import models

class tipoContenido(models.Model):
    """
    Esta clase representa un tipo de Contenido dentro del sistema.
    Atributos:
    - nombre: Nombre representativo del tipo de Contenido.
    - descripcion: Descripcion del tipo de Contenido.
    Ejemplo:    nombre: Wiki
                descripcion: Contenido del tipo Wiki
    """
    nombre = models.CharField(max_length=30, unique=True)
    descripcion = models.CharField(max_length=200)

    def __str__(self):

        """
        Este metodo retorna el nombre y la descripcion del tipo de Contenido.
        :return: Se retorna un str
        """

        return f"{self.nombre} : {self.descripcion}"
    @classmethod
    def crear(cls, nombre, descripcion):

        """
        Este metodo sirve para crear un tipo de Contenido
        :nombre: Nombre del tipo de Contenido a crear (str)
        :descripcion: Descripcion del tipo de Contenido a crear (str)
        :return: Retorna el tipo de Contenido
        """

        tipoDContenido = tipoContenido(nombre=nombre, descripcion=descripcion)
        tipoDContenido.save()
        return tipoDContenido

    def eliminar(self):

        """
        Metodo que elimina el rol correspondiente a la instancia actual
        """

        self.delete()

    @classmethod
    def eliminar_por_nombre(cls, nombre):

        """
        Esta funcion elimina un tipo de Contenido por el nombre que es recibido como parametro
        :nombre: Nombre del tipo de Contenido (str)
        """

        cls.objects.filter(nombre=nombre).delete()

    @classmethod
    def obtener_por_nombre(cls, nombre):

        """
        Obtenemos un tipo de Contenido por el nombre
        :nombre: El nombre por el cual buscaremos el tipo de Contenido (str)
        :return: (tipoContenido)
        """

        try:
            return cls.objects.get(nombre=nombre)
        except cls.DoesNotExist:
            return None

    @classmethod
    def obtener_todos(cls):

        """
        Obtenemos todas los tipos de Contenidos
        :return: (tipoContenido-list)
        """

        return cls.objects.all()

    @classmethod
    def getById(cls, id):

        """
        Obtenemos un tipo de Contenido por el id
        :id: El id por el cual buscaremos el tipo de Contenido (int)
        :return: (tipoContenido)
        """

        return cls.objects.get(id=id)

    class Meta:
        verbose_name = "tipo de contenido"
        verbose_name_plural = "tipos de contenido"
        db_table = "tipo_de_contenido"
