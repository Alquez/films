# Generated by Django 4.2.1 on 2023-06-12 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0019_remove_comment_name_comment_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='user',
        ),
        migrations.AddField(
            model_name='comment',
            name='name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
