# Generated by Django 4.2.5 on 2023-10-31 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenido', '0007_contenido_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='contenido',
            name='numero_vistas',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='contenido',
            name='titulo',
            field=models.CharField(default='titulo', max_length=200),
        ),
    ]