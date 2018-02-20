from datetime import datetime

import requests
from bs4 import BeautifulSoup
from django.shortcuts import render, redirect
from artist.models import Artist

def artist_list(request):
    # 전체 Artist목록을 ul>li로 출력
    # 템플릿은 'artist/artist_list.html'을 사용
    # 전달할 context 키는 'artists'를 사용
    artists = Artist.objects.all()
    context = {
        'artists': artists,
    }
    return render(request, 'artist/artist_list.html', context)


def artist_create(request):
    context = {

    }

    if request.method == 'POST':
        name = request.POST['name']
        real_name = request.POST['real_name']
        nationality = request.POST['nationality']
        birth_date = request.POST['birth_date']
        constellation = request.POST['constellation']
        blood_type = request.POST['blood_type']
        intro = request.POST['intro']

        artist = Artist.objects.create(
            name=name,
            real_name=real_name,
            nationality=nationality,
            constellation=constellation,
            blood_type=blood_type,
            intro=intro,
            # strptime 문자열을 날짜와 시간으로 바꿈
            birth_date=datetime.strptime(birth_date, '%Y-%m-%d')
        )
        artist.save()
        return redirect('artist:artist-list')

    elif request.method == 'GET':
        pass

    return render(request, 'artist/artist_create.html', context)


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

