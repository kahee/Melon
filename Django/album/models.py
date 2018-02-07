from django.db import models

# Create your models here.
from artist.models import Artist


class Album(models.Model):
    album_name = models.CharField('앨범명', max_length=100)
    # 가수 : 앨범  = 1 : N
    artist = models.ForeignKey(
        '가수명',
        Artist,
        on_delete=models.SET_NULL,
    )
    release_date = models.DateField('발매일', )
    genre = models.CharField('장르', max_length=100)
    album_intro = models.TextField('앨범소개', blank=True)
