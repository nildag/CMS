# Generated by Django 4.2.5 on 2023-11-28 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notify', '0003_alter_notification_destiny'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='tipo_accion',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
