# Generated by Django 4.2.5 on 2023-10-05 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='tipoContenido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30, unique=True)),
                ('descripcion', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'tipo de contenido',
                'verbose_name_plural': 'tipos de contenido',
                'db_table': 'tipo_de_contenido',
            },
        ),
    ]
