from datetime import datetime

import requests
from bs4 import BeautifulSoup
from django.core.files.base import ContentFile

__all__ = (
    'album_detail_crawler',
)


def album_detail_crawler(album_id):
    url = "https://www.melon.com/album/detail.htm"
    params = {
        'albumId': album_id,
    }

    response = requests.get(url, params)
    soup = BeautifulSoup(response.text, 'lxml')

    album_title = soup.find('div', class_="song_name").strong.next_sibling.strip()
    album_cover_url = soup.find('a', id='d_album_org').img.get('src')
    meta = soup.find('dl', class_='list.py')
    rel_date = meta.find('dd').get_text(strip=True)

    result_dic = dict()
    result_dic["album_title"] = album_title
    result_dic["album_cover"] = album_cover_url
    result_dic["rel_date"] = rel_date

    return result_dic
