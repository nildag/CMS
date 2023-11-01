from django.db.models.signals import pre_delete
from django.dispatch import receiver
from tipoContenido.models import tipoContenido
from contenido.models import Contenido

@receiver(pre_delete, sender=tipoContenido)
def asignar_tipo_por_defecto_a_contenidos(sender, instance, **kwargs):
    contenidos_asociados = Contenido.objects.filter(tipoContenido=instance)
    nuevo_tipo_por_defecto = tipoContenido.objects.get(nombre='Sin tipo')  # Reemplaza 'Nuevo Tipo por Defecto' con el nombre del nuevo tipo por defecto
    contenidos_asociados.update(tipoContenido=nuevo_tipo_por_defecto)
