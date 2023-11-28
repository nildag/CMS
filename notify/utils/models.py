# ContentType
from django.contrib.contenttypes.fields import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# --------
from django.db import models
from django.contrib.auth.models import Group
from django.db.models.query import QuerySet
# Timezone
from django.utils import timezone
# load_model
from swapper import load_model
from notify.signals import notificar
from usuario.models import User


class NotificationQueryset(models.QuerySet):
    def leido(self):
        """
        Retorna las notificacion que hayan sido leidas en el actual Queryset
        :param include_deleted:
        :return:
        """
        return self.filter(read=True)

    def no_leido(self):
        """
        Retorna solo los items que no hayan sido leidos en el actual Queryset
        :param include_deleted:
        :return:
        """
        return self.filter(read=False).count()

    def marcar_todo_como_leido(self, destiny=None):
        """
        Marcar todas las notify como leidas en el actual queryset
        :param destiny:
        :return:
        """
        qs = self.read(False)
        if destiny:
            qs = qs.filter(destiny=destiny)
        return qs.update(read=True)

    def marcar_todo_como_no_leido(self, destiny=None):
        """
        Marcar todas las notify como no leidas en el actual queryset
        :param destiny:
        :return:
        """
        qs = self.read(True)
        if destiny:
            qs = qs.filter(destiny=destiny)

        return qs.update(read=False)


class AbstractNotificationManager(models.Manager):
    def get_queryset(self):
        return self.NotificationQueryset(self.Models, using=self._db)


class AbstractNotificacion(models.Model):
    class Levels(models.TextChoices):
        success = 'Success', 'success',
        info = 'Info', 'info',
        wrong = 'Wrong', 'wrong'

    level = models.CharField(choices=Levels.choices, max_length=20, default=Levels.info)

    destiny = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificacion', blank=True, null=True)

    actor_content_type = models.ForeignKey(ContentType, related_name='notificar_actor', on_delete=models.CASCADE)
    object_id_actor = models.PositiveIntegerField()
    actor = GenericForeignKey('actor_content_type', 'object_id_actor')

    verbo = models.CharField(max_length=220)

    read = models.BooleanField(default=False)
    publico = models.BooleanField(default=True)
    eliminado = models.BooleanField(default=False)

    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    tipo_accion = models.CharField(max_length=50, blank=True, null=True)

    objects = NotificationQueryset.as_manager()

    class Meta:
        abstract = True

    def __str__(self):
        return "Actor: {} ---- Destiny: {} ".format(self.actor, self.destiny)


def notify_signals(verb, **kwargs):
    """
    Funcion de controlador para crear una instancia de notificacion tras
    una llamada de signal de accion
    :param verb:
    :param kwargs:
    :return:
    """
    print("Notificación generada:", verb)
    #destiny = kwargs.pop('destiny')
    actor = kwargs.pop('sender')

    publico = bool(kwargs.pop('publico', True))
    timestamp = kwargs.pop('timestamp', timezone.now())

    Notify = load_model('notify', 'Notification')
    levels = kwargs.pop('level', Notify.Levels.info)

    categoria_destino = kwargs.pop('categoria_destino', None)
    tipo_accion = kwargs.pop('tipo_accion', None)

    str_tipo_accion = ""

    if tipo_accion== "Edicion":
        str_tipo_accion = "Editor"
    elif tipo_accion == "Publicacion":
        str_tipo_accion = "Publicador"

    if categoria_destino:
        # Obtén a los usuarios editores de la categoría
        users_with_editor_role = User.objects.filter(
            usercategoria__rol__nombre=str_tipo_accion,
            usercategoria__categoria=categoria_destino
        )

        new_notify = []
        for user in users_with_editor_role:
            notification = Notify(
                destiny=user,
                actor_content_type=ContentType.objects.get_for_model(actor),
                object_id_actor=actor.pk,
                verbo=str(verb),
                publico=publico,
                timestamp=timestamp,
                level=levels,
                tipo_accion=tipo_accion,
            )
            notification.save()
            new_notify.append(notification)
        return new_notify


notificar.connect(notify_signals, dispatch_uid='notify.models.Notification')
