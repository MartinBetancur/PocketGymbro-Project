# Generated by Django 5.0.1 on 2024-05-21 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gymapp', '0022_lesiones_fecha'),
    ]

    operations = [
        migrations.AddField(
            model_name='historial',
            name='comentarios',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='historial',
            name='opinion',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], default=5),
        ),
    ]