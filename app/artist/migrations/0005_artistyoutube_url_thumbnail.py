# Generated by Django 2.0.2 on 2018-02-28 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0004_auto_20180228_0220'),
    ]

    operations = [
        migrations.AddField(
            model_name='artistyoutube',
            name='url_thumbnail',
            field=models.CharField(blank=True, max_length=200, verbose_name='썸네일'),
        ),
    ]