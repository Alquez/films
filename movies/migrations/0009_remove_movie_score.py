# Generated by Django 4.2.1 on 2023-06-02 06:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0008_ratingstar_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='score',
        ),
    ]