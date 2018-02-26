from datetime import datetime

from django.conf import settings
from django.core.files import File
from django.db import models

# Create your models here.
from crawler import album_detail_crawler
from utils.file import download, get_buffer_ext


def dynamic_ablum_cover_path(instance, filename):
    return f'album/{instance.title}-{instance.album_id}/album_cover.png'


class AlbumManager(models.Manager):
    def update_or_creaet_from_album_id(self, album_id):
        album_info = album_detail_crawler(album_id)

        # 이미지 파일로 만드는 것
        # 객체가져오기만 하는
        # 예외처리경우, 앨범이미지가 없는 경우도 있다.
        temp_file = download(album_info['album_cover'])
        file_name = '{album_id}.{exe}'.format(
            album_id=album_id,
            exe=get_buffer_ext(temp_file),
        )

        album, album_created = Album.objects.get_or_create(
            album_id=album_id,
            defaults={
                'release_date': datetime.strptime(album_info.get("rel_date"), '%Y.%m.%d'),
                'title': album_info.get("album_title"),
            }
        )
        album.img_cover.save(file_name, File(temp_file))

        return album, album_created


class Album(models.Model):
    album_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    title = models.CharField('앨범명', max_length=100)

    img_cover = models.ImageField(
        '커버 이미지',
        upload_to='album',
        blank=True,
    )
    release_date = models.DateField('발매일', )
    # 장르는 가지고 있는 노래들에서 가져오기

    album_intro = models.TextField('앨범소개', blank=True)

    # 앨범을 좋아요 누른 사람
    like_user = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='like_album',
        blank=True,
    )

    @property
    def genre(self):
        # sql distinct사용하는게 속도가 더 빠르다.
        return ', '.join(self.song_set.values_list('genre', flat=True).distinct())

    def __str__(self):
        return self.title
        # # 호호호빵 (휘성, 김태우)
        # artists = ', '.join(self.artists.values_list('name', flat=True))
        # return '{title} [{artists}]'.format(
        #     title=self.title,
        #     artists=artists,
        # )

    objects = AlbumManager()


class AlbumLike(models.Model):
    album = models.ForeignKey(
        Album,
        related_name='like_user_info_list',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='like_album_info_list',
        on_delete=models.CASCADE,
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        unique_together = (
            ('album', 'user'),
        )

    def __str__(self):
        return 'AlbumLike (User:{user}, Album:{album}, Created:{created})'.format(
            album=self.album,
            user=self.user,
            created=datetime.strftime(self.created_date,'%Y.%m.%d'),

        )
