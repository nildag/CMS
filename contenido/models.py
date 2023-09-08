from django.db import models
from django.contrib.auth.models import Permission

class Contenido (models.Model):
    class Meta:
        default_permissions = ()
        permissions = (
                ('crear_contenido', 'Crear contenido'),
                ('editar_contenido', 'Editar contenido'),
                ('publicar_contenido', 'Publicar contenido'),
        )