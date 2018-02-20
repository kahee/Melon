import re
import requests
from bs4 import BeautifulSoup


def get_search_artist(keyword):
    url = 'https://www.melon.com/search/artist/index.htm'
    params = {
        'q': keyword,
        'section': 'searchGnbYn'
    }

    response = requests.get(url, params)

    print(response.url)

    soup = BeautifulSoup(response.text, 'lxml')

    artist_info = soup.find_all('div', class_='wrap_atist12')
    result = []
    for i in artist_info:
        # 아티스트 이미지
        artist_img = i.find('a', class_="thumb").find('img').get('src')
        # 아티스트 고유번호
        artist_id_href = i.find('a', class_="ellipsis").get('href')
        artist_id = re.search(r"\('(\d+)'\);", artist_id_href).group(1)
        # 아티스트 이름
        artist = i.find('a', class_="ellipsis").text
        # 아티스트 정보
        info = i.find('dd', class_="gubun").get_text(strip=True)
        # 아티스트 장르
        genre = i.find('dd', class_="gnr").get_text(strip=True)[4:]
        result.append({
            'artist_id': artist_id,
            'artist': artist,
            'info': info,
            'genre': genre,
            'img' :artist_img,
        })
    return result


if __name__ == '__main__':
    artists = get_search_artist('아이유')
    for artist in artists:
        print(artist)
