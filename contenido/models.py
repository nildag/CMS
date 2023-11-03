from django.db import models
from usuario.models import User
from categorias.models import Categoria
from tipoContenido.models import tipoContenido
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.conf import settings  # Importa la configuración de Django
from django.contrib.auth.models import User

class Contenido(models.Model):
    
    """
    Modelo para almacenar el contenido creado por los usuarios.

    Atributos:
        - titulo (str): Título del contenido.
        - cuerpo (RichTextField): Cuerpo del contenido en formato rico.
        - autor (User): Usuario que crea el contenido.
        - categoria (Categoria): Categoría a la que pertenece el contenido.
        - tipo_contenido (TipoContenido): Tipo de contenido.
        - fecha_creacion (datetime): Fecha y hora de creación del contenido.
        - puntuacion (Decimal): Puntuación promedio del contenido.
        - numero_valoraciones (int): Número total de valoraciones del contenido.
        - estado (str): Estado del contenido. Puede ser 'Borrador', 'Edicion', 'Publicacion' o 'Deshabilitado'.

    Métodos:
        - for_user(user): Devuelve los contenidos creados por un usuario específico.
        - for_categorias(categorias): Devuelve los contenidos asociados a una lista de categorías.
    """
    titulo = models.CharField(max_length=200, default="titulo")
    cuerpo = RichTextField(default="cuerpo")
    #autor = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, default=1)
    tipo_contenido = models.ForeignKey(tipoContenido, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    # Nuevos campos para valoración
    puntuacion = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    numero_valoraciones = models.PositiveIntegerField(default=0)
    numero_vistas = models.PositiveIntegerField(default=0)
    estado = models.CharField(max_length=30, default="Borrador")

    def __str__(self):
        return f"{self.titulo} - {self.autor.first_name} {self.autor.last_name}"

    class Meta:
        verbose_name = "Contenido"
        verbose_name_plural = "Contenidos"
        db_table = "contenido"

    @classmethod
    def for_user(self, user):
        """
        Devuelve una lista de contenidos creados por un usuario específico.

        Args:
            user (User): El usuario para el que se obtienen los contenidos.

        Returns:
            QuerySet: Una lista de objetos de contenido creados por el usuario.

        Example:
            Para obtener los contenidos creados por el usuario 'alice', puedes usar:
            contenidos = Contenido.for_user(User.objects.get(username='alice'))
        """

        return Contenido.objects.filter(autor=user)
    
    @classmethod
    def for_categorias(self, categorias):

        """
        Funcion que devuelve los contenidos de una lista de categorias
        :param categorias: lista de categorias (Categoria)
        :return: lista de contenidos de las categorias
        """

        return Contenido.objects.filter(categoria__in=categorias)

class Valoracion(models.Model):
    """
    Modelo que representa una valoración de contenido.

    Atributos:
        contenido (Contenido): El contenido que se valora.
        usuario (User): El usuario que realiza la valoración.
        puntuacion (int): La puntuación otorgada, generalmente en un rango de 1 a 5.
        fecha (datetime): La fecha y hora en que se creó la valoración.

    Métodos:
        __str__(): Devuelve una representación legible de la valoración.

    Atributos:
        contenido (Contenido): El contenido que se valora.
        usuario (User): El usuario que realiza la valoración.
        puntuacion (int): La puntuación otorgada, generalmente en un rango de 1 a 5.
        fecha (datetime): La fecha y hora en que se creó la valoración.
    """

    contenido = models.ForeignKey(Contenido, on_delete=models.CASCADE)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    puntuacion = models.PositiveIntegerField()  # Aquí puedes usar un rango de 1 a 5, por ejemplo
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Devuelve una representación legible de la valoración.
        :return: Cadena con el formato "Valoración de [nombre de usuario] para [título del contenido]".
        """
        return f"Valoración de {self.usuario.username} para {self.contenido.titulo}"
