from django.db import models
from permiso.models import Permiso

class Rol(models.Model):

    """
    Esta clase representa un Rol dentro del sistema.
    Atributos:
    - nombre: Nombre representativo del rol. Ejemplo: Autor (str)
    - descripcion: Descripcion de lo que representa el rol. Ejemplo: Rol que se encargara de la creacion de contenidos dentro del sistema (str)
    - permisos: Atributo correspondiente a los permisos que posee el rol (ManyToManyField)
    """

    nombre = models.CharField(max_length=30, unique=True)
    descripcion = models.CharField(max_length=100)
    permisos = models.ManyToManyField(Permiso)
    last_modification = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"
        db_table = "rol"

    def __str__(self):

        """
        Este metodo retorna el nombre y la descripcion del rol.
        :return: Se retorna un str
        """
        
        return f"{self.nombre} : {self.descripcion}"
    
    @classmethod
    def getAll(cls):

        """
        Este metodo retorna todos los roles que existen en el sistema.
        :return: Se retorna un QuerySet
        """

        return Rol.objects.all()
    
    @classmethod
    def getByNombre(cls, nombre):
            
        """
        Este metodo retorna un rol en especifico.
        :param nombre: Nombre del rol que se desea obtener (str)
        :return: Se retorna un Rol
        """
    
        return Rol.objects.get(nombre=nombre)