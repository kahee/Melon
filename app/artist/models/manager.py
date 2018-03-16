from django.core.files import File
from django.db import models

from crawler import artist_detail_crawler
from utils.file import download, get_buffer_ext

__all__ = (
    'ArtistManager',
)


class ArtistManager(models.Manager):
    # def to_json(self):
    #     return = []
    #
    #     for instance in self.get_queryset():
    #         result.appen
    #
    #     artist_list = [artist for artist in self.values('pk', 'melon_id', 'name', 'img_profile',)]
    #
    #     # Artists.objects.to_dict()
    #     # [
    #     #     {
    #     #         'pk':<artist:pk>,
    #     #         'name':<artist:name>,
    #     #         'img_profile':<artist:img_profile>,
    #     #     }
    #     # ]
    #     return artist_list

    def update_or_create_from_melon(self, artist_id):

        # 기존 쿼리셋 self.get_queryset()
        # 특정 쿼리셋의 데이터 리스트를 dict의 list형태로 반환하
        from .artist import Artist
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
