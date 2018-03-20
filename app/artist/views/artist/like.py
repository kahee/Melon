from django.shortcuts import redirect

from artist.models import Artist


def artist_like(request, artist_pk):
    """
    request.user와 artist_pk를 사용해서 ArtistLike 객체를 토글하는 뷰
    완료 후에는  artist:artist-list로 이동
    :param request:
    :param artist_pk:
    :return:

    1. 좋아요 버튼을 누른다(template에서 받음)
    2. artist_pk가 request.user에 있는지 확인
    3. 없으면 생성 있으면 지우는 버전 -> toggle_like_artist
    """

    if request.method == "POST":
        artist = Artist.objects.get(pk=artist_pk)
        artist.toggle_like_user(request.user)
        # next-path가 있는지 없는지에 따라 redirect 페이지가 달라짐
        next_path = request.POST.get('next-path', 'artist:artist-list')
        return redirect(next_path)
