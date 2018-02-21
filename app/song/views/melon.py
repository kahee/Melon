import requests

from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST
from crawler.song import song_list_crawler, song_detail_crawler
from song.models import Song

__all__ = [
    'song_search_from_melon',
    'song_add_from_melon',
]



# 405 오류
@require_GET
def song_search_from_melon(request):

    keyword = request.GET.get('keyword')

    result = song_list_crawler(keyword)

    context = {
        'result': result,
    }

    return render(request, 'song/song_search_from_melon.html', context)


@require_POST
def song_add_from_melon(request):
    song_id = request.POST.get('song_id')

    result = song_detail_crawler(song_id)

    Song.objects.update_or_create(
        song_id=song_id,
        defaults={
            'title': result.get('title'),
            'genre': result.get('genre'),
            'lyrics': result.get('lyrics'),
        }
    )

    return redirect('song:song-list')
