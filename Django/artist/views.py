from datetime import datetime

from django.shortcuts import render, redirect

# Create your views here.
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



