# Generated by Django 4.2.5 on 2023-11-01 21:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tipoContenido', '0001_initial'),
        ('contenido', '0010_alter_contenido_tipo_contenido'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contenido',
            name='tipo_contenido',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tipoContenido.tipocontenido'),
        ),
    ]
