from django.shortcuts import redirect
from ...models import Artist

__all__ = (
    'artist_add_from_melon',
)


def artist_add_from_melon(request):
    """
    post 요청을 받음
    artist_id 를 사용해서
    멜론 사이트에서 Artist 에 들어갈 상세 정보 가져오기

    artist_id
    name
    real_name
    birth_date

    nationality
    constellation
    blood_type

    intro를 채운 artist를 생성 db에 저장
    :return:

     """
    if request.method == 'POST':
        artist_id = request.POST.get('artist_id')
        artist, _ = Artist.objects.update_or_create_from_melon(artist_id)

    return redirect('artist:artist-list.py')
