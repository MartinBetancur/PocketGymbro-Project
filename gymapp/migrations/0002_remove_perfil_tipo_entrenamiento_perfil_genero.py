# Generated by Django 5.0.3 on 2024-04-02 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gymapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perfil',
            name='tipo_entrenamiento',
        ),
        migrations.AddField(
            model_name='perfil',
            name='genero',
            field=models.TextField(default=None),
        ),
    ]