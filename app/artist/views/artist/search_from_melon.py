import re
import requests
from bs4 import BeautifulSoup
from django.shortcuts import render


__all__ = (
    'artist_search_from_melon',
)


def artist_search_from_melon(request):
    """
    Tmplate : artist/artist_add_from_melon.htmlm
        from input  한개,  button 한개
    1. form에 주어진 'keyword'로 멜론 사이트의 아티스트 검색 결과를 크롤링
    2. 크롤링 된 검색결과를 적절히 파싱해서 검색 결과 목록을 생성
         -> list내에  dict들을 만드는 형태
    3. 해당 결과 목록을 템플릿에 출력
        -> list 내에 dict 들을 만드는 형태
        artist_info_list = [
        {'name':'아이유', 'url_img_cover': 'http..'
    :param request:
    :return:
    """

    keyword = request.GET.get('keyword')
    context = {}
    if keyword:
        url = 'https://www.melon.com/search/artist/index.htm'
        params = {
            'q': keyword,
            'section': 'searchGnbYn'
        }

        response = requests.get(url, params)

        soup = BeautifulSoup(response.text, 'lxml')

        artist_info = soup.find_all('div', class_='wrap_atist12')
        artist_info_list = []
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
            artist_info_list.append({
                'artist_id': artist_id,
                'artist': artist,
                'info': info,
                'genre': genre,
                'img': artist_img,
            })

        context['artist_info_list'] = artist_info_list

    return render(request, 'artist/artist_search_from_melon.html',context)
