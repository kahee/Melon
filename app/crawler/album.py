import requests
from bs4 import BeautifulSoup
from django.core.files.base import ContentFile


def album_detail_crawler(album_id):
    url = "https://www.melon.com/album/detail.htm"
    params = {
        'albumId': album_id,
    }

    response = requests.get(url, params)
    soup = BeautifulSoup(response.text, 'lxml')

    album_title = soup.find('div', class_="song_name").strong.next_sibling.strip()
    album_cover_url = soup.find('a', id='d_album_org').img.get('src')

    # 이미지 파일로 만드는 것
    # 객체가져오기만 하는
    # 예외처리경우, 앨범이미지가 없는 경우도 있다.
    binary_data = requests.get(album_cover_url).content
    album_cover = ContentFile(binary_data, name="album_cover.png")

    meta = soup.find('dl', class_='list')
    rel_date = meta.find('dd').get_text(strip=True)

    result_dic = dict()

    result_dic["album_title"] = album_title
    result_dic["album_cover"] = album_cover
    result_dic["rel_date"] = rel_date

    return result_dic
