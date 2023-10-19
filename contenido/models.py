from django.db import models
from usuario.models import User
from categorias.models import Categoria
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.conf import settings  # Importa la configuración de Django
from django.contrib.auth.models import User

class Contenido(models.Model):
    """
    Modelo para almacenar el contenido creado por los usuarios.

    Atributos:
        titulo (str): Título del contenido.
        cuerpo (RichTextField): Cuerpo del contenido en formato rico.
        autor (User): Usuario que crea el contenido.
        categoria (Categoria): Categoría a la que pertenece el contenido.
        fecha_creacion (datetime): Fecha y hora de creación del contenido.
    """
    titulo = models.CharField(max_length=30, default="titulo")
    cuerpo = RichTextField(default="cuerpo")
    #autor = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, default=1)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    # Nuevos campos para valoración
    puntuacion = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    numero_valoraciones = models.PositiveIntegerField(default=0)
    def __str__(self):
        return f"{self.titulo} - {self.autor.first_name} {self.autor.last_name}"

    class Meta:
        verbose_name = "Contenido"
        verbose_name_plural = "Contenidos"
        db_table = "contenido"

class Valoracion(models.Model):
    contenido = models.ForeignKey(Contenido, on_delete=models.CASCADE)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    puntuacion = models.PositiveIntegerField()  # Aquí puedes usar un rango de 1 a 5, por ejemplo
    fecha = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Valoración de {self.usuario.username} para {self.contenido.titulo}"


    @classmethod
    def for_user(self, user):

        """
        Funcion que devuelve los contenidos de un usuario
        :param user: usuario a comprobar (User)
        :return: lista de contenidos del usuario
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
