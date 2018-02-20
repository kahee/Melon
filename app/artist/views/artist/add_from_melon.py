from datetime import datetime
import re
import requests
from bs4 import BeautifulSoup
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from ...models import Artist

__all__ = (
    'artist_add_from_melon',
)


def artist_add_from_melon(request):
    """
    post 요청을 받음
    artist_id 를 사용해서
    멜론 사이트에서 Artist 에 들어갈 상세 정보 가져오기

    artist_id
    name
    real_name
    birth_date

    nationality
    constellation
    blood_type

    intro를 채운 artist를 생성 db에 저장
    :return:
    # """
    if request.method == 'POST':
        artist_id = request.POST.get('artist_id')

        print(artist_id)
        url = 'https://www.melon.com/artist/detail.htm'
        params = {
            'artistId': artist_id
        }

        response = requests.get(url, params)
        print(response.url)

        soup = BeautifulSoup(response.text, 'lxml')

        # 기본 정보 _info
        wrap_dtl_atist = soup.find('div', class_='wrap_dtl_atist')
        url_img_cover = wrap_dtl_atist.find('span', id="artistImgArea").find('img').get('src')
        name_div = wrap_dtl_atist.select_one('p.title_atist').text[5:]
        name = re.search(r'(\w+)\s', name_div).group(1)
        real_name = re.search(r'\((\w+)\)', name_div).group(1)
        birthday = wrap_dtl_atist.select_one('dl.atist_info > dd:nth-of-type(2)').get_text(strip=True)

        # _personal_information
        dl_list_define = soup.find('div', class_="section_atistinfo04").find('dl', class_='list_define')

        personal_list = list()
        for index, i in enumerate(dl_list_define.find_all("dd")):
            personal_list.append(i.get_text(strip=True))

        personal_information = {
            "본명": personal_list[0],
            "별명": personal_list[1],
            "국적": personal_list[2],
            "생일": personal_list[3],
            "별자리": personal_list[4],
            "혈액형": personal_list[5]
        }

        db_name = name
        db_real_name = real_name
        db_birth_date = birthday
        db_nationality = personal_list[2]
        db_constellation = personal_list[4]
        db_blood_type = personal_list[5]

        for short, full in Artist.CHOICES_BLOOD_TYPE:
            if db_blood_type.strip() == full:
                db_blood_type = short
                break
            else:
                db_blood_type = Artist.BLOOD_TYPE_X

        Artist.objects.update_or_create(
            melon_id=artist_id,
            defaults={
                'name': db_name,
                'real_name': db_real_name,
                'nationality': db_nationality,
                'constellation': db_constellation,
                'birth_date': datetime.strptime(db_birth_date, '%Y.%m.%d'),
                'blood_type': db_blood_type,
            }
        )

    return redirect('artist:artist-list')
