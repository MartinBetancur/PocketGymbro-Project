# Generated by Django 5.0.1 on 2024-05-20 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gymapp', '0021_lesiones_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesiones',
            name='fecha',
            field=models.DateField(default=None),
        ),
    ]