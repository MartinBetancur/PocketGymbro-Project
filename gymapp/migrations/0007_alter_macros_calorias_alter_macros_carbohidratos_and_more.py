# Generated by Django 5.0.1 on 2024-05-19 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gymapp', '0006_macros'),
    ]

    operations = [
        migrations.AlterField(
            model_name='macros',
            name='calorias',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='macros',
            name='carbohidratos',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='macros',
            name='grasas',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='macros',
            name='proteinas',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
