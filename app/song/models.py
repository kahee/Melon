from django.db import models
from album.models import Album


class Song(models.Model):
    song_id = models.CharField('song_id', max_length=50, unique=True, blank=True, null=True)
    album = models.ForeignKey(
        Album,
        verbose_name='앨범',
        on_delete=models.CASCADE,
        blank=True,
        null=True,

    )
    title = models.CharField('곡 제', max_length=100, )
    # 가수 : 곡 = 1: N
    genre = models.CharField(
        '장르',
        max_length=100,
    )

    lyrics = models.TextField('가사', blank=True, )

    @property
    def artists(self):
        return ', '.join(self.album.artists.values_list('name', flat=True))

    @property
    def release_date(self):
        return self.album.release_date

    @property
    def formatted_release_date(self):
        return self.release_date.strftime('%Y.%m.%d')

    def __str__(self):
        # 가수명 - 곡제목 (앨범명)
        return self.title