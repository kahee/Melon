import datetime
from django.shortcuts import redirect, render

from ...models import Artist

__all__ = (
    'artist_create',
)


def artist_create(request):
    context = {}

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
