# Generated by Django 4.2.5 on 2023-10-02 15:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contenido', '0004_alter_contenido_cuerpo'),
    ]

    operations = [
        migrations.AddField(
            model_name='contenido',
            name='fecha_creacion',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
