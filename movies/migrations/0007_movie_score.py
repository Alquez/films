# Generated by Django 4.2.1 on 2023-06-01 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_delete_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='score',
            field=models.IntegerField(blank=True, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True),
        ),
    ]
