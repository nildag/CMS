from django.db import models
from django.contrib.auth.models import AbstractUser
from rol.models import Rol
from categorias.models import Categoria
from permiso.models import Permiso
from django.utils import timezone
from django.db.models.signals import post_save
from notify.signals import notificar


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

    def tiene_permiso_en_categoria(self, permiso, categoria):
        """
        Este método retorna si el usuario actual tiene un permiso dado en una categoría dada.
        :param permiso: Permiso que se desea verificar (str)
        :param categoria: Categoría en la que se desea verificar el permiso (Categoria)
        :return: Se retorna un bool
        """
        userCategorias = UserCategoria.objects.filter(user=self)
        for userCategoria in userCategorias:
            if userCategoria.categoria == categoria:
                if userCategoria.rol.tiene_permiso(permiso):
                    return True
        return False

    def admin_roles(self):

        """
        Este método retorna si el usuario actual es administrador de roles.
        :return: Se retorna un bool
        """

        system = Categoria.objects.get(nombre="System")
        permiso = "Administrar roles"
        tiene_permiso = self.tiene_permiso_en_categoria(permiso, system)
        return tiene_permiso

    def admin_categorias(self):

        """
        Este método retorna si el usuario actual es administrador de categorías.
        :return: Se retorna un bool
        """

        system = Categoria.objects.get(nombre="System")
        permiso = "Administrar categorias"
        tiene_permiso = self.tiene_permiso_en_categoria(permiso, system)
        return tiene_permiso

    def admin_asigRoles(self):

        """
        Este método retorna si el usuario actual es administrador de asignación de roles.
        :return: Se retorna un bool
        """

        system = Categoria.objects.get(nombre="System")
        permiso = "Asignar roles"
        tiene_permiso = self.tiene_permiso_en_categoria(permiso, system)
        return tiene_permiso

    def admin_tipo_contenido(self):

        """
        Este método retorna si el usuario actual es administrador de tipo de contenido.
        :return: Se retorna un bool
        """

        system = Categoria.objects.get(nombre="System")
        permiso = "Administrar tipo de contenido"
        tiene_permiso = self.tiene_permiso_en_categoria(permiso, system)
        return tiene_permiso

    def user_is_autor(self):

        """
        Este método retorna si el usuario actual es autor.
        :return: Se retorna un bool
        """

        categorias = Categoria.objects.all()
        for categoria in categorias:
            if categoria.nombre != "System" and self.tiene_permiso_en_categoria("Crear contenido", categoria):
                return True
        return False

    def is_publicador(self):

        """
        Este método retorna si el usuario actual es publicador.
        :return: Se retorna un bool
        """

        categorias = Categoria.objects.all()
        for categoria in categorias:
            if self.tiene_permiso_en_categoria("Publicar contenido", categoria):
                return True
        return False

    def is_editor(self):

        """
        Este método retorna si el usuario actual es editor.
        :return: Se retorna un bool
        """

        categorias = Categoria.objects.all()
        for categoria in categorias:
            if self.tiene_permiso_en_categoria("Editar contenido", categoria):
                return True
        return False


class UserCategoria(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        """
        Este método retorna los datos del usuario.
        :return: Se retorna un str
        """
        return f"{self.user} : {self.rol} : {self.categoria}"

    @classmethod
    def getByUser(user):
        """
        Este método retorna todos los roles que tiene un usuario.
        :return: Se retorna un QuerySet
        """
        return UserCategoria.objects.filter(user=user)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.FileField(upload_to='fotos')
    text = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    def __str__(self):
        return self.title


def notify_post(sender, instance, created, **kwargs):
    notificar.send(instance.user, destiny=instance.user, verb=instance.title, level='success')


post_save.connect(notify_post, sender=Post)
