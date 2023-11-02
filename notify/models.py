
from notify.utils.models import AbstractNotificacion
from django.db import models

class Notification(AbstractNotificacion):
    class Meta(AbstractNotificacion.Meta):
        abstract = False
