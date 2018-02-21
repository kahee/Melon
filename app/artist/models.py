from django.db import models


# instance 저장되는 객체 ,  filename은 저장 이름
# 저장 -> pre_save -> save -> post_save -> 끝
# pre_save때 이미지에 none으로 데이터베이스에 저장
# post_save때 다시 원래 이미지를 넣어줌

def dynamic_profile_img_path(instance, filename):
    # pk로 받으면 instance가 저장이 안되서 pk가없다.
    return f'artist/{instance.name}-{instance.melon_id}/profile_img.png'


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
    img_profile = models.ImageField('프로필 이미지', upload_to=dynamic_profile_img_path, blank=True)
    name = models.CharField('이름', max_length=50, )
    real_name = models.CharField('본명', max_length=30, blank=True, )
    nationality = models.CharField('국적', max_length=50, blank=True, )
    birth_date = models.DateField('생년월일', blank=True, null=True, )
    constellation = models.CharField('별자리', max_length=30, blank=True, )
    blood_type = models.CharField('혈액형', max_length=1, choices=CHOICES_BLOOD_TYPE, blank=True)
    intro = models.TextField('소개', blank=True, )
    melon_id = models.CharField('멜론 ArtistID', max_length=20, blank=True, null=True, unique=True, )

    def __str__(self):
        return self.name
