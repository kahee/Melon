from django.db import models

# Create your models here.
from artist.models import Artist


class Video(models.Model):
    video_id = models.CharField('videoID', max_length=200, blank=True)
    title = models.CharField('제목', max_length=200, blank=True)
    img_url = models.ImageField('썸네일', upload_to='artist', blank=True)
    artists = models.ManyToManyField(
        Artist,
        verbose_name='아티스트 목록',
        blank=True,
    )

    def __str__(self):
        return f'{self.video_id} - {self.title}'
