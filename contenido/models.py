from django.db import models
from usuario.models import User
from categorias.models import Categoria
from ckeditor.fields import RichTextField

class Contenido (models.Model):


    titulo = models.CharField(max_length=30,default="titulo")
    #cuerpo = models.CharField(max_length=500,default="cuerpo")
    cuerpo = RichTextField(default="cuerpo")
    autor=models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    categoria=models.ForeignKey(Categoria, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.autor.first_name} {self.autor.last_name}"

    class Meta:
        verbose_name = "Contenido"
        verbose_name_plural = "Contenidos"
        db_table = "contenido"