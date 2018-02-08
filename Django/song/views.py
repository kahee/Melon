from django.shortcuts import render

# Create your views here.
from song.models import Song


def song_list(request):
    songs = Song.objects.all()
    context = {
        'songs':songs
    }

    return render(request,'song/song_list.html',context)