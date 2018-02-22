from datetime import datetime

from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from artist.models import Artist
from crawler.artist_data import artist_detail_crawler
from ...models import Album
from ...models import Song
from crawler.album import album_detail_crawler
from crawler.song import song_detail_crawler


@require_POST
def song_add_from_melon(request):
    song_id = request.POST.get('song_id')

    result = song_detail_crawler(song_id)

    artist_id = result.get('artist_id')
    artist_info = artist_detail_crawler(artist_id)

    birth_date = artist_info['birth_date']
    blood_type = artist_info['blood_type']

    if blood_type != '':
        for short, full in Artist.CHOICES_BLOOD_TYPE:
            if blood_type.strip() == full:
                blood_type = short
                break

    else:
        blood_type = Artist.BLOOD_TYPE_X

    artist, _ = Artist.objects.get_or_create(
        artist_id=artist_id,
        defaults={
            'name': artist_info['name'],
            'real_name': artist_info['real_name'],
            'nationality': artist_info['nationality'],
            'constellation': artist_info['constellation'],
            'birth_date': birth_date,
            'blood_type': blood_type,
            'img_profile': artist_info['img_profile'],
        }
    )

    album_id = result.get('album_id')
    album_info = album_detail_crawler(album_id)

    album, created = Album.objects.get_or_create(
        album_id=album_id,
        defaults={
            'img_cover': album_info.get('album_cover'),
            'release_date': datetime.strptime(album_info.get("rel_date"), '%Y.%m.%d'),
            'title': album_info.get("album_title"),
        }
    )

    Song.objects.update_or_create(
        song_id=song_id,
        defaults={
            'title': result.get('title'),
            'genre': result.get('genre'),
            'lyrics': result.get('lyrics'),
            'album': album
        }
    )

    return redirect('song:song-list')
