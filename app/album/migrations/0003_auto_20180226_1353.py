# Generated by Django 2.0.2 on 2018-02-26 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0002_auto_20180226_1307'),
    ]

    operations = [
        migrations.RenameField(
            model_name='album',
            old_name='like_user',
            new_name='like_users',
        ),
    ]
