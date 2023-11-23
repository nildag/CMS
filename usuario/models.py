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
    
    def obtener_categorias_por_permiso(self, permiso):
        """
        Este método retorna las categorías en las que el usuario tiene un permiso dado pasado como parámetro.
        :param permiso: Permiso que se desea verificar (str)
        :return: Se retorna un QuerySet
        """
        categorias = Categoria.objects.all()
        categorias_con_permiso = []
        for categoria in categorias:
            if self.tiene_permiso_en_categoria(permiso, categoria):
                categorias_con_permiso.append(categoria)
        return categorias_con_permiso
    
    def is_autor_in_categoria(self, categoria):
        """
        Este método retorna si el usuario actual tiene el rol Autor en una categoría dada.
        :param categoria: Categoría en la que se desea verificar si el usuario es autor (Categoria)
        :return: Se retorna un bool
        """
        userCategorias = UserCategoria.objects.filter(user=self)
        for userCategoria in userCategorias:
            if userCategoria.categoria == categoria:
                if userCategoria.rol.nombre == "Autor":
                    return True
        return False
    
    def tiene_permiso_en_categoria(self, permiso, categoria):
        """
        Este método retorna si el usuario actual tiene un permiso dado en una categoría dada. Si se recibe null en categoria, se verifica en todas las categorías.
        :param permiso: Permiso que se desea verificar (str)
        :param categoria: Categoría en la que se desea verificar el permiso (Categoria)
        :return: Se retorna un bool
        """
        userCategorias = UserCategoria.objects.filter(user=self)
        for userCategoria in userCategorias:
            if categoria is None or userCategoria.categoria == categoria:
                permisos = Permiso.objects.filter(rol=userCategoria.rol)
                for permisoRol in permisos:
                    if permisoRol.nombre == permiso:
                        return True
        return False
    
    @classmethod
    def obtener_usuarios_sin_permiso(cls, permiso):
        """
        Este método retorna los usuarios que no tienen un permiso dado.
        :param permiso: Permiso que se desea verificar (str)
        :return: Se retorna un QuerySet
        """
        usuarios = User.objects.all()
        usuarios_sin_permiso = []
        for usuario in usuarios:
            if not usuario.tiene_permiso_en_categoria(permiso, None):
                usuarios_sin_permiso.append(usuario)
        return usuarios_sin_permiso
    
    def tiene_permiso_asignar_roles(self):
        """
        Este método retorna si el usuario actual tiene el permiso "Asignar roles"
        :return: Se retorna un bool
        """
        return self.tiene_permiso_en_categoria("Asignar roles", None)
    
    def tiene_permiso_administrar_tipoContenido(self):
        """
        Este método retorna si el usuario actual tiene el permiso "Administrar tipo de contenido" en la categoría System, atendiendo que dicho permiso solo tiene sentido en la categoría System.
        :return: Se retorna un bool
        """
        system = Categoria.objects.get(nombre="System")
        return self.tiene_permiso_en_categoria("Administrar tipo de contenido", system)
    
    def tiene_permiso_administrar_roles(self):
        """
        Este método retorna si el usuario actual tiene el permiso "Administrar roles" en la categoría System, atendiendo que dicho permiso solo tiene sentido en la categoría System.
        :return: Se retorna un bool
        """
        system = Categoria.objects.get(nombre="System")
        return self.tiene_permiso_en_categoria("Administrar roles", system)
    
    def tiene_permiso_administrar_categorias(self):
        """
        Este método retorna si el usuario actual tiene el permiso "Administrar categorías" en la categoría System, atendiendo que dicho permiso solo tiene sentido en la categoría System.
        :return: Se retorna un bool
        """
        system = Categoria.objects.get(nombre="System")
        return self.tiene_permiso_en_categoria("Administrar categorias", system)
    
    def tiene_permiso_visualizar_kanban(self):
        """
        Este método retorna si el usuario actual tiene el permiso "Visualizar kanban" en la categoría System, atendiendo que dicho permiso solo tiene sentido en la categoría System.
        :return: Se retorna un bool
        """
        system = Categoria.objects.get(nombre="System")
        return self.tiene_permiso_en_categoria("Visualizar Kanban", system)
    
    def tiene_permiso_crear_contenido(self):
        """
        Este método retorna si el usuario actual tiene el permiso "Crear contenido" en alguna categoría.
        :return: Se retorna un bool
        """
        return self.tiene_permiso_en_categoria("Crear contenido", None)
    
    def tiene_permiso_eliminar_contenido(self):
        """
        Este método retorna si el usuario actual tiene el permiso "Eliminar contenido" en alguna categoría.
        :return: Se retorna un bool
        """
        return self.tiene_permiso_en_categoria("Eliminar contenido", None)
    
    def tiene_permiso_editar_contenido(self):
        """
        Este método retorna si el usuario actual tiene el permiso "Editar contenido" en alguna categoría.
        """
        return self.tiene_permiso_en_categoria("Editar contenido", None)
    
    def tiene_permiso_publicar_contenido(self):
        """
        Este método retorna si el usuario actual tiene el permiso "Publicar contenido" en alguna categoría.
        """
        return self.tiene_permiso_en_categoria("Publicar contenido", None)

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
