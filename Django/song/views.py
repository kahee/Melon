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

    if request.method == 'POST':
        # POST요청에 전달된 INPUT요소 중, name이 'keyword'인 input 값
        # 공백문자 삭제 .strip()
        keyword = request.POST['keyword'].strip()

        # keyword에 빈 문자열이 들어갔을 경우, QuerySet을 실행하지 않
        if not keyword:
            pass

        else:
            # Song목록 중 title이 keyword 를 포함하는 쿼리셋
            # 빈값이 들어왔을 때는 all이 들어간거랑 마찬가지
            songs = Song.objects.filter(title__contains=keyword)
            # 미리 선언한  context의 'songs'키에  QuerySet을 할당
            context['songs'] = songs

    # 만약 method가 post이면 context에 'songs' 가 채워진 상태,
    # GET이면 빈 태로 render실행
    return render(request, 'song/song_search.html', context)
