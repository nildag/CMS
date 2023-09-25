from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Esta clase representa un usuario dentro del sistema por medio del sso.
    """
    # Campos personalizados nombre y apellido

    def __str__(self):
        """
        Este método retorna los datos del usuario.
        :return: Se retorna un str
        """
        return f"{self.username} : {self.first_name} : {self.last_name} : {self.email}"
