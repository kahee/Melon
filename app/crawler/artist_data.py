import re
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from django.core.files.base import ContentFile

__all__ = (
    'artist_detail_crawler',
)


def artist_detail_crawler(artist_id):
    url = 'https://www.melon.com/artist/detail.htm'
    params = {
        'artistId': artist_id
    }
    response = requests.get(url, params)

    soup = BeautifulSoup(response.text, 'lxml')

    # _personal_information
    div_section_atistinfo04 = soup.find('div', class_="section_atistinfo04")
    if not div_section_atistinfo04 == None:
        dl = div_section_atistinfo04.find('dl', class_='list_define')
        items = [item.get_text(strip=True) for item in dl.contents if not isinstance(item, str)]
        li = iter(items)
        personal_information = dict(zip(li, li))

    # 기본 info 이미지, 이름, 본명
    wrap_dtl_atist = soup.find('div', class_='wrap_dtl_atist')
    url_img_cover = wrap_dtl_atist.find('span', id="artistImgArea").find('img').get('src')

    # 이미지가 없을 경우에는 url 주소가 없는 것처럼
    if url_img_cover == "http://cdnimg.melon.co.kr":
        url_img_cover = ""

    name = wrap_dtl_atist.select_one('p.title_atist').contents[1]
    real_name = personal_information.get('본명', '')
    birth_date = personal_information.get('생일', '')
    nationality = personal_information.get('국적', '')
    constellation = personal_information.get('별자리', '')
    blood_type = personal_information.get('혈액형', '')

    # birth_date_str 이 없을 때 처리하기
    if birth_date == '':
        birth_date = None
    else:
        birth_date = datetime.strptime(birth_date, '%Y.%m.%d')

    # 이미지 넣는 코드부분
    # 그림파일형태의 이미지 가져옴
    response = requests.get(url_img_cover)
    binary_data = response.content

    from pathlib import Path
    file_name = Path(url_img_cover).name
    img_profile = ContentFile(binary_data, name=file_name)

    artist_info = {}

    artist_info[' artist_id'] = artist_id
    artist_info['name'] = name
    artist_info['real_name'] = real_name
    artist_info['birth_date'] = birth_date
    artist_info['nationality'] = nationality
    artist_info['blood_type'] = blood_type
    artist_info['constellation'] = constellation
    artist_info['img_profile'] = img_profile

    return artist_info
