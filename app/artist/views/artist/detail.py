import requests
from django.shortcuts import render, get_object_or_404

from config.settings import YOUTUBE_API_KEY
from video.models import Video
from ...models import Artist

__all__ = (
    'artist_detail',
)


def artist_detail(request, artist_pk):
    # artist_pk에 해당하는 Artist정보 보여주기
    # Template: artist/artist_detail.html

    artist = get_object_or_404(Artist, pk=artist_pk)

    key = YOUTUBE_API_KEY
    url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'key': key,
        'part': 'snippet',
        'type': 'video',
        'maxResult': '10',
        'q': artist.name,
    }

    response = requests.get(url, params)
    response_dict = response.json()

    context = {
        'artist': artist,
        'youtube_items': response_dict['items'],
    }

    return render(request, 'artist/artist_detail.html', context)
