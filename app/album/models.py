from django.db import models

# Create your models here.
from artist.models import Artist

def dynamic_ablum_cover_path(instance, filename):
    return f'album/{instance.title}-{instance.album_id}/album_cover.png'

class Album(models.Model):
    album_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    title = models.CharField('앨범명', max_length=100)

    artists = models.ManyToManyField(
        Artist,
        verbose_name='아티스트 목록'
    )
    img_cover = models.ImageField(
        '커버 이미지',
        upload_to=dynamic_ablum_cover_path,
        blank=True,
    )
    release_date = models.DateField('발매일', )
    # 장르는 가지고 있는 노래들에서 가져오기

    album_intro = models.TextField('앨범소개', blank=True)

    @property
    def genre(self):
        # sql distinct사용하는게 속도가 더 빠르다.
        return ', '.join(self.song_set.values_list('genre', flat=True).distinct())

    def __str__(self):
        # 호호호빵 (휘성, 김태우)
        artists = ', '.join(self.artists.values_list('name', flat=True))
        return '{title} [{artists}]'.format(
            title=self.title,
            artists=artists,
        )
