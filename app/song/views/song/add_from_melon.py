from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from ...models import Song


@require_POST
def song_add_from_melon(request):
    if request.method == 'POST':
        # Song.objects.update_or_create_from_melon_id()  메서드를 SongManager에 만들고
        # 해당 메서드가 Song_detail 정보들을 저장하면서 Artist.objects.update_or_create_from_melon_id()도 호출
        # song_detail 정보 db에 저장
        # artist_detail 정보 db에 저장
        song_id = request.POST.get('song_id')
        song, _ = Song.objects.update_or_create_from_melon_id(song_id)

        # 0. AlbumManager  만들기
        # 1. album 모델에 update_or_create_from_album_id ()
        # 2. song _update_or_create_form_melon_id 에 추가하기


        # album_detail 정보 db에 저장





    return redirect('song:song-list')
