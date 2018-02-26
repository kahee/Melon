from datetime import timezone, datetime

from django.conf import settings
from django.core.files import File
from django.db import models

# instance 저장되는 객체 ,  filename은 저장 이름
# 저장 -> pre_save -> save -> post_save -> 끝
# pre_save때 이미지에 none으로 데이터베이스에 저장
# post_save때 다시 원래 이미지를 넣어줌
from crawler.artist_data import artist_detail_crawler
from utils.file import download, get_buffer_ext


def dynamic_profile_img_path(instance, filename):
    # pk로 받으면 instance가 저장이 안되서 pk가없다.
    return f'artist/{instance.name}-{instance.melon_id}/profile_img.png'


class ArtistManager(models.Manager):

    def update_or_create_from_melon(self, artist_id):

        artist_info = artist_detail_crawler(artist_id)
        birth_date = artist_info['birth_date']
        blood_type = artist_info['blood_type']

        if blood_type != '':
            for short, full in Artist.CHOICES_BLOOD_TYPE:
                if blood_type.strip() == full:
                    blood_type = short
                    break

        else:
            blood_type = Artist.BLOOD_TYPE_X

        #  매니저 객체에 있는 update_or_create를 사용할 예정

        artist, artist_created = self.update_or_create(
            melon_id=artist_id,
            defaults={
                'name': artist_info['name'],
                'real_name': artist_info['real_name'],
                'nationality': artist_info['nationality'],
                'constellation': artist_info['constellation'],
                'birth_date': birth_date,
                'blood_type': blood_type,
            }
        )

        temp_file = download(artist_info['img_profile'])
        file_name = '{artist_id}.{exe}'.format(
            artist_id=artist_id,
            exe=get_buffer_ext(temp_file),
        )
        # ModelManager 로 utils 함수를 만드는 편이 낫다.
        # 파일 중복 저장
        if artist.img_profile:
            # 이전에 이미지 파일이 있으면 이전 파일을 삭제 후, 새로 저장
            artist.img_profile.delete()
        artist.img_profile.save(file_name, File(temp_file))

        return artist, artist_created


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

    objects = ArtistManager()


class ArtistLike(models.Model):
    # Artist와 User(members.User)와의 관계를 나타내주는
    artist = models.ForeignKey(
        Artist,
        related_name='like_user_info_list',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='like_artist_info_list',
        on_delete=models.CASCADE,
    )
    created_date = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        # 같은 유저가 같은 아티스트 좋아요 누르는게 중복 되지 않게
        unique_together = (
            ('artist', 'user'),
        )

    def __str__(self):
        return 'ArtistLike (User:{user}, Artist:{artist}, Created:{created})'.format(
            artist=self.artist,
            user=self.user.username,
            created=datetime.strftime(self.created_date, '%Y.%m.%d'),
        )
