from django.conf import settings
from django.db import models

from .artist_youtube import ArtistYouTube
# from artist.models import ArtistYouTube
# 이경우 init에서 ArtistYouTube 를 만들기 전에 불러서 오류
from .manager import ArtistManager



__all__ = (
    'Artist',
)


class Artist(models.Model):
    BLOOD_TYPE_A = 'a'
    BLOOD_TYPE_B = 'b'
    BLOOD_TYPE_O = 'o'
    BLOOD_TYPE_C = 'c'
    BLOOD_TYPE_X = 'x'

    CHOICES_BLOOD_TYPE = (
        (BLOOD_TYPE_A, 'A형'),
        (BLOOD_TYPE_B, 'B형'),
        (BLOOD_TYPE_O, 'O형'),
        (BLOOD_TYPE_C, 'AB형'),
        (BLOOD_TYPE_X, '기타'),
    )

    # Pillow 이미지 저장하기 위해 사용하는 것
    melon_id = models.CharField('멜론 ArtistID', max_length=20, blank=True, null=True, unique=True, )
    img_profile = models.ImageField('프로필 이미지', upload_to='artist', blank=True)
    name = models.CharField('이름', max_length=50, )
    real_name = models.CharField('본명', max_length=30, blank=True, )
    nationality = models.CharField('국적', max_length=50, blank=True, )
    birth_date = models.DateField('생년월일', blank=True, null=True, )
    constellation = models.CharField('별자리', max_length=30, blank=True, )
    blood_type = models.CharField('혈액형', max_length=1, choices=CHOICES_BLOOD_TYPE, blank=True)
    intro = models.TextField('소개', blank=True, )

    # 노래에 좋아요를 누른 유저
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="ArtistLike",
        related_name='like_artists',
        blank=True,
    )

    youtube_videos = models.ManyToManyField(
        ArtistYouTube,
        related_name='artists',
        blank=True,
    )

    objects = ArtistManager()

    def __str__(self):
        return self.name

    def toggle_like_user(self, user):
        """
        주어진 like_user에 주어진 user가 자신의 like_user에 없으면
         like_users 에 추가한다

        이미 있는 경우
        :param user:
        :return:
        """
        # 자신이 'artist' 이미 user가 주어진 user인 ArtistLike를 가져오거나 없으면 생성
        like, like_created = self.like_user_info_list.get_or_create(user=user)
        # 만약 이미 있었을 경우(새로 생성되지 않았을 경우)
        if not like_created:
            # like를 지워줌
            like.delete()
        # 생성 여부를 알려줌
        return like_created

