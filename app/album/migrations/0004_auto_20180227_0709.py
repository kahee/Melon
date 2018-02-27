# Generated by Django 2.0.2 on 2018-02-27 07:09

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0003_auto_20180226_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='like_users',
            field=models.ManyToManyField(blank=True, related_name='like_album', through='album.AlbumLike', to=settings.AUTH_USER_MODEL),
        ),
    ]
