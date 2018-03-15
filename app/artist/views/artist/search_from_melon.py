from django.shortcuts import render

from crawler.artist_data import artist_list_crawler

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
        -> list.py 내에 dict 들을 만드는 형태
        artist_info_list = [
        {'name':'아이유', 'url_img_cover': 'http..'
    :param request:
    :return:
    """
    context = dict()
    keyword = request.GET.get('keyword')
    artist_info_list = artist_list_crawler(keyword)
    context['artist_info_list'] = artist_info_list

    return render(request, 'artist/artist_search_from_melon.html', context)
