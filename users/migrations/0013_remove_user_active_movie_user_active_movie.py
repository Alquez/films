# Generated by Django 4.2.1 on 2023-05-30 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_remove_movie_user'),
        ('users', '0012_alter_user_active_movie'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='active_movie',
        ),
        migrations.AddField(
            model_name='user',
            name='active_movie',
            field=models.ManyToManyField(blank=True, null=True, to='movies.movie'),
        ),
    ]
