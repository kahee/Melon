from django.shortcuts import render

# Create your views here.
from album.models import Album


def album_list(request):
    albums = Album.objects.all()

    context = {
        'albums': albums
    }

    return render(request, 'album/album_list.html', context)

