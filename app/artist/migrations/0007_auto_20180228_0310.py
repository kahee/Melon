# Generated by Django 2.0.2 on 2018-02-28 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0006_auto_20180228_0310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artistyoutube',
            name='url_thumbnail',
            field=models.URLField(blank=True, verbose_name='커버 이미지 URL'),
        ),
    ]
