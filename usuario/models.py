from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Esta clase representa un usuario dentro del sistema por medio del sso.
    Atributos:
    -username: Nombre de usuario del dentro del sistema.
    - email: Email del usuario.
    - nombre: Nombre del usuario.
    - apellido: Apellido del usuario.
    """
    # Campos personalizados nombre y apellido
    nombre = models.CharField(max_length=30, blank=False)
    apellido = models.CharField(max_length=50, blank=False)

    def __str__(self):
        """
        Este método retorna los datos del usuario.
        :return: Se retorna un str
        """
        return f"{self.username} : {self.first_name} : {self.last_name} : {self.email}"
