from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from song.models import Song


def song_list(request):
    songs = Song.objects.all()
    context = {
        'songs': songs
    }
    return render(request, 'song/song_list.html', context)


def song_serarch(request):
    """
    사용할 url : song/search/
    사용할 템플릿 :templates/song/song_search.html
        form
    input, button

    1. input의 name= keyword로 지정
    2. 이 함수를 request.method가 'get'일 때와 'post'일때로 분기
    3. request.method가 ' Post'일 때 request.POST dict 'name'키에 해당하는 값을
    httpresponse로 출력
    4. request.method가 'get'일 때, 이전에 하던 템플릿 출력을 유지

    - Query filter로 검색하기
    1. keyword가 자신의 'title'에 포함되는 Song쿼리셋 생성
    2. 위 쿼리셋을 'soongs'변수에 할당
    3. context dict 를 만들고 'songs'키에 songs변수 할당
    4. render의 3번째 인수로 context를 전달
    5. template에 전달된 ' songs'를 출력

    :param request:
    :return:
    """
    context = {}
    # Song과 연결된 Artist의 name에 keyword가 포함된 경우
    # Song과 연결된 Album의 title에 keyword가 포함된 경우를
    # 모두 포함(or-> Q objects)하는 쿼리셋을 'songs'에 할당

    # songs_from_artists
    # songs_from_albums
    # songs_from_title
    # 위 세 변수에 더 위의 조건 3개에 부합하는 쿼리셋을 각각 전달
    # 세 변수를 이용해서 검색 결과를 3단으로 분리해서 출력
    # ex) 아티스트로 검색한 노래 결과, 앨범으로 검색한 노래 결과, 제목으로 검색한 노래 결과 출력
    #  템플릿도 수정할 것

    if request.method == 'POST':
        # POST요청에 전달된 INPUT요소 중, name이 'keyword'인 input 값
        # 공백문자 삭제 .strip()
        keyword = request.POST['keyword'].strip()

        # keyword에 빈 문자열이 들어갔을 경우, QuerySet을 실행하지 않기
        if not keyword:
            pass

        else:
            songs_from_artists = Song.objects.filter(album__artists__name__contains=keyword).distinct()
            songs_from_albums = Song.objects.filter(album__title__contains=keyword)
            songs_from_title = Song.objects.filter(title__contains=keyword)

            context['songs_from_artists'] = songs_from_artists
            context['songs_from_albums'] = songs_from_albums
            context['songs_from_title'] = songs_from_title

            # Song목록 중 title이 keyword 를 포함하는 쿼리셋
            # 빈값이 들어왔을 때는 all이 들어간거랑 마찬가지
        #     songs = Song.objects.filter(
        #     Q(album__title__contains=keyword) |
        #     Q(album__artists__name__contains=keyword) |
        #     Q(title__contains=keyword)
        # ).distinct()
        # 미리 선언한  context의 'songs'키에  QuerySet을 할당
        # context['songs'] = songs

        # 만약 method가 post이면 context에 'songs' 가 채워진 상태,
        # GET이면 빈 태로 render실행

    return render(request, 'song/song_search.html', context)
