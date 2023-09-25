from django.db import models
from django.contrib.auth.models import AbstractUser
from rol.models import Rol
from categorias.models import Categoria

class User(AbstractUser):

    """
    Esta clase representa un usuario dentro del sistema por medio del sso.
    """

    # Campos personalizados
    roles = models.ManyToManyField(Rol, related_name='roles', through="UserCategoria", blank=True)

    def __str__(self):
        """
        Este método retorna los datos del usuario.
        :return: Se retorna un str
        """
        return f"{self.username} : {self.first_name} : {self.last_name} : {self.email}"

class UserCategoria(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
