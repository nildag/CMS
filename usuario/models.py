from django.db import models
from django.contrib.auth.models import AbstractUser
from rol.models import Rol
from categorias.models import Categoria

class User(AbstractUser):

    """
    Esta clase hereda de AbstractUser y se encarga de almacenar los datos de los usuarios.
    - roles: Atributo correspondiente a los roles que posee el usuario (ManyToManyField)
    - registrado: Atributo que indica si el usuario se encuentra registrado o no (bool)
    """

    # Campos personalizados
    roles = models.ManyToManyField(Rol, related_name='roles', through="UserCategoria", blank=True)
    registrado = models.BooleanField(default=True)

    def __str__(self):
        """
        Este método retorna los datos del usuario.
        :return: Se retorna un str
        """
        return f"{self.username} : {self.first_name} : {self.last_name} : {self.email}"
    
    @classmethod
    def getAll(cls):
        """
        Este método retorna todos los usuarios que existen en el sistema.
        :return: Se retorna un QuerySet
        """
        return User.objects.all()
    
    def user_autor(user):

        """
        Funcion que verifica si el usuario es autor en alguna categoria
        :param user: usuario
        :return: True si el usuario es autor, False si no lo es (boolean)
        """

        return UserCategoria.objects.filter(user=user, rol__nombre='Autor').values_list('categoria__id', flat=True)

class UserCategoria(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
