from datetime import datetime
import re
import requests
from bs4 import BeautifulSoup
from django.core.files.base import ContentFile
from django.shortcuts import redirect
from io import BytesIO

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

     """
    if request.method == 'POST':

        artist_id = request.POST.get('artist_id')

        url = 'https://www.melon.com/artist/detail.htm'
        params = {
            'artistId': artist_id
        }
        response = requests.get(url, params)
        print(response.url)

        soup = BeautifulSoup(response.text, 'lxml')

        # _personal_information
        div_section_atistinfo04 = soup.find('div', class_="section_atistinfo04")
        if not div_section_atistinfo04 == None:
            dl = div_section_atistinfo04.find('dl', class_='list_define')
            items = [item.get_text(strip=True) for item in dl.contents if not isinstance(item, str)]
            li = iter(items)
            personal_information = dict(zip(li, li))
            print(personal_information)

        # 기본 info 이미지, 이름, 본명
        wrap_dtl_atist = soup.find('div', class_='wrap_dtl_atist')
        url_img_cover = wrap_dtl_atist.find('span', id="artistImgArea").find('img').get('src')

        # 이미지가 없을 경우에는 url 주소가 없는 것처럼
        if url_img_cover == "http://cdnimg.melon.co.kr":
            url_img_cover = ""

        name = wrap_dtl_atist.select_one('p.title_atist').contents[1]
        print(name)
        print(url_img_cover)
        print(artist_id)

        db_name = name
        db_real_name = personal_information.get('본명')
        db_birth_date = personal_information.get('생일')
        db_nationality = personal_information.get('국적')
        db_constellation = personal_information.get('별자리')
        db_blood_type = personal_information.get('혈액형')

        # blood_type과 birth_date_str 이 없을 때 처리하기
        if db_birth_date == '':
            db_birth_date = None
        else:
            db_birth_date = datetime.strptime(db_birth_date, '%Y.%m.%d')

        if not db_blood_type:
            for short, full in Artist.CHOICES_BLOOD_TYPE:
                if db_blood_type.strip() == full:
                    db_blood_type = short
                    break

            else:
                db_blood_type = Artist.BLOOD_TYPE_X

        # 이미지 넣는 코드부분
        # 그림파일형태의 이미지 가져옴
        response = requests.get(url_img_cover)
        binary_data = response.content

        # # BytesIO 파일처럼 취급하는 객체인데, 메모리상에서만
        # # 아무런 내용이 없는 파일이 메모리에 생성
        # temp_file = BytesIO()
        # # 그 파일에 데이터를 입력
        # temp_file.write(binary_data)
        # # 파일 탐색 시점 처음으로
        # # 어떠한 데이터가 입력된 파일 데이터
        # # 임시 파일이기때문에 이름이 없다.
        # temp_file.seek(0)

        from pathlib import Path
        file_name = Path(url_img_cover).name

        artist, _ = Artist.objects.update_or_create(
            melon_id=artist_id,
            defaults={
                'name': db_name,
                'real_name': db_real_name,
                'nationality': db_nationality,
                'constellation': db_constellation,
                'birth_date': db_birth_date,
                'blood_type': db_blood_type,
                'img_profile': ContentFile(binary_data, name=file_name)
            }
        )

        return redirect('artist:artist-list')


from datetime import datetime
import re
import requests
from bs4 import BeautifulSoup
from django.core.files.base import ContentFile
from django.shortcuts import redirect
from io import BytesIO

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

     """
    if request.method == 'POST':

        artist_id = request.POST.get('artist_id')

        url = 'https://www.melon.com/artist/detail.htm'
        params = {
            'artistId': artist_id
        }
        response = requests.get(url, params)
        print(response.url)

        soup = BeautifulSoup(response.text, 'lxml')

        # _personal_information
        div_section_atistinfo04 = soup.find('div', class_="section_atistinfo04")
        if not div_section_atistinfo04 == None:
            dl = div_section_atistinfo04.find('dl', class_='list_define')
            items = [item.get_text(strip=True) for item in dl.contents if not isinstance(item, str)]
            li = iter(items)
            personal_information = dict(zip(li, li))
            print(personal_information)

        # 기본 info 이미지, 이름, 본명
        wrap_dtl_atist = soup.find('div', class_='wrap_dtl_atist')
        url_img_cover = wrap_dtl_atist.find('span', id="artistImgArea").find('img').get('src')

        # 이미지가 없을 경우에는 url 주소가 없는 것처럼
        if url_img_cover == "http://cdnimg.melon.co.kr":
            url_img_cover = ""

        name = wrap_dtl_atist.select_one('p.title_atist').contents[1]
        print(name)
        print(url_img_cover)
        print(artist_id)

        db_name = name
        db_real_name = personal_information.get('본명', '')
        db_birth_date = personal_information.get('생일', '')
        db_nationality = personal_information.get('국적', '')
        db_constellation = personal_information.get('별자리', '')
        db_blood_type = personal_information.get('혈액형', '')

        # blood_type과 birth_date_str 이 없을 때 처리하기
        if db_birth_date == '':
            db_birth_date = None
        else:
            db_birth_date = datetime.strptime(db_birth_date, '%Y.%m.%d')

        if db_blood_type != '':
            for short, full in Artist.CHOICES_BLOOD_TYPE:
                if db_blood_type.strip() == full:
                    db_blood_type = short
                    break

        else:
            db_blood_type = Artist.BLOOD_TYPE_X

        # 이미지 넣는 코드부분
        # 그림파일형태의 이미지 가져옴
        response = requests.get(url_img_cover)
        binary_data = response.content

        # # BytesIO 파일처럼 취급하는 객체인데, 메모리상에서만
        # # 아무런 내용이 없는 파일이 메모리에 생성
        # temp_file = BytesIO()
        # # 그 파일에 데이터를 입력
        # temp_file.write(binary_data)
        # # 파일 탐색 시점 처음으로
        # # 어떠한 데이터가 입력된 파일 데이터
        # # 임시 파일이기때문에 이름이 없다.
        # temp_file.seek(0)

        from pathlib import Path
        file_name = Path(url_img_cover).name

        artist, _ = Artist.objects.update_or_create(
            melon_id=artist_id,
            defaults={
                'name': db_name,
                'real_name': db_real_name,
                'nationality': db_nationality,
                'constellation': db_constellation,
                'birth_date': db_birth_date,
                'blood_type': db_blood_type,
                'img_profile': ContentFile(binary_data, name=file_name)
            }
        )

        return redirect('artist:artist-list')
