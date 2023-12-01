
from notify.utils.models import AbstractNotificacion
from django.db import models

class Notification(AbstractNotificacion):
    class Meta(AbstractNotificacion.Meta):
        abstract = False

    def __str__(self):
        actor_name = getattr(self.actor, 'get_full_name', None) or str(self.actor)
        return f"Actor: {actor_name} ---- Destiny: {self.destiny}"

