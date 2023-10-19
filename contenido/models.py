from django.db import models
from usuario.models import User
from categorias.models import Categoria
from django.utils import timezone
from ckeditor.fields import RichTextField

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
    autor = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, default=1)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.titulo} - {self.autor.first_name} {self.autor.last_name}"

    class Meta:
        verbose_name = "Contenido"
        verbose_name_plural = "Contenidos"
        db_table = "contenido"

    @classmethod
    def for_user(self, user):

        """
        Funcion que devuelve los contenidos de un usuario
        :param user: usuario a comprobar (User)
        :return: lista de contenidos del usuario
        """

        return Contenido.objects.filter(autor=user)