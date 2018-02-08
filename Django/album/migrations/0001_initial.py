# Generated by Django 2.0.2 on 2018-02-08 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('artist', '0002_auto_20180206_0757'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='앨범명')),
                ('img_cover', models.ImageField(blank=True, upload_to='album', verbose_name='커버 이미지')),
                ('release_date', models.DateField(verbose_name='발매일')),
                ('album_intro', models.TextField(blank=True, verbose_name='앨범소개')),
                ('artists', models.ManyToManyField(to='artist.Artist', verbose_name='아티스트 목록')),
            ],
        ),
    ]
