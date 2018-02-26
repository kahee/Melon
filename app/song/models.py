from datetime import datetime

from django.conf import settings
from django.db import models
from album.models import Album
from artist.models import Artist
from crawler.song_data import song_detail_crawler


class SongManager(models.Manager):
    def update_or_create_from_melon_id(self, song_id):
        """
        song_id에 해당하는 Song정보를 멜론사이트에서 가져와 update_or_create를 실행
        이 때, 해당 Song의 Artist정보도 가져와 ArtistManager.update_or_create_from_melon도 실행
        :param song_id: 멜론 사이트에서의 곡 고유 ID
        :return: (Song instance, Bool(Song created))
        """
        result = song_detail_crawler(song_id)
        artist_id = result.get('artist_id')
        album_id = result.get('album_id')
        album, _ = Album.objects.update_or_creaet_from_album_id(album_id)
        artist, _ = Artist.objects.update_or_create_from_melon(artist_id)
        song, song_created = Song.objects.update_or_create(
            song_id=song_id,
            defaults={
                'title': result.get('title'),
                'genre': result.get('genre'),
                'lyrics': result.get('lyrics'),
                'album': album,
            }
        )
        # 생성된  Song의 artists의 필드를 추가
        song.artists.add(artist)

        return song, song_created


class Song(models.Model):
    song_id = models.CharField('song_id', max_length=50, unique=True, blank=True, null=True)

    album = models.ForeignKey(
        Album,
        verbose_name='앨범',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    artists = models.ManyToManyField(
        Artist,
        verbose_name='아티스트 목록',
        blank=True,
    )

    title = models.CharField('곡 제', max_length=100, )
    # 가수 : 곡 = 1: N
    genre = models.CharField(
        '장르',
        max_length=100,
    )

    lyrics = models.TextField('가사', blank=True, )

    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="SongLike",
        related_name='like_song',
        blank=True,
    )

    def toggle_like_user(self, user):
        like, like_created = self.like_user_info_list.get_or_create(user=user)
        # 만약 이미 있었을 경우(새로 생성되지 않았을 경우)
        if not like_created:
            # like를 지워줌
            like.delete()
        # 생성 여부를 알려줌
        return like_created

    @property
    def release_date(self):
        return self.album.release_date

    @property
    def formatted_release_date(self):
        return self.release_date.strftime('%Y.%m.%d')

    def __str__(self):
        # 가수명 - 곡제목 (앨범명)
        # if self.album:
        #     return '{artists} - {title} ({album})'.format(
        #         artists=', '.join(self.album.artists.values_list('name', flat=True)),
        #         title=self.title,
        #         album=self.album.title,
        #     )
        #
        # else:
        return self.title

    objects = SongManager()


class SongLike(models.Model):
    song = models.ForeignKey(
        Song,
        related_name='like_user_info_list',
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='like_song_info_list',
        on_delete=models.CASCADE,
    )
    created_date = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = (
            ('song', 'user'),
        )

    def __str__(self):
        return 'SongLike (User:{user}, Song:{song}, Created:{created})'.format(
            artist=self.song,
            user=self.user.username,
            created=datetime.strftime(self.created_date, '%Y.%m.%d'),
        )
