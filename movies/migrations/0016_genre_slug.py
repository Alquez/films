# Generated by Django 4.2.1 on 2023-06-06 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0015_rename_actors_actor'),
    ]

    operations = [
        migrations.AddField(
            model_name='genre',
            name='slug',
            field=models.SlugField(default=1),
        ),
    ]