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
    :param request:
    :return:
    """
    return render(request,'song/song_search.html',{})

