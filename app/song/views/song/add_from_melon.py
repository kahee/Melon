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
    if request.method == 'POST':
        # Song.objects.update_or_create_from_melon()  메서드를 SongManager에 만들고
        # 해당 메서드가 Song_detail 정보들을 저장하면서 Artist.objects.update_or_create_from_melon()도 호출
        # song_detail 정보 db에 저장
        # artist_detail 정보 db에 저장
        song_id = request.POST.get('song_id')
        song, _ = Song.objects.update_or_create_from_melon(song_id)

        # album_detail 정보 db에 저장
        # album_id = result.get('album_id')
        # album_info = album_detail_crawler(album_id)
        #
        # album, created = Album.objects.get_or_create(
        #     album_id=album_id,
        #     defaults={
        #         'img_cover': album_info.get('album_cover'),
        #         'release_date': datetime.strptime(album_info.get("rel_date"), '%Y.%m.%d'),
        #         'title': album_info.get("album_title"),
        #     }
        # )


    return redirect('song:song-list')
