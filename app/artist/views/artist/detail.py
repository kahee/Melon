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
        'q': artist.name,
    }
    response = requests.get(url, params)
    response_dict = response.json()

    video_lists = list()

    for item in response_dict['items']:
        video_id = item['id']['videoId']
        title = item['snippet']['title']
        img_url = item['snippet']['thumbnails']['medium']['url']

        video_url = 'https://www.youtube.com/watch'
        params = {
            'v': video_id,
        }

        href = requests.get(video_url, params).url

        video_lists.append({
            'video_id': video_id,
            'title': title,
            'img_url': img_url,
            'name': artist.name,
            'href': href,
        })

    context = {
        'artist': artist,
        'video_lists': video_lists,

    }

    return render(request, 'artist/artist_detail.html', context)
