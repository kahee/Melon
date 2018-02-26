from django.shortcuts import render

from artist.models import Artist

__all__ = (
    'artist_list',
)


def artist_list(request):
    # 전체 Artist목록을 ul>li로 출력
    # 템플릿은 'artist/artist_list.html'을 사용
    # 전달할 context 키는 'artists'를 사용
    artists = Artist.objects.all()
    context = {
        'artists': artists,
    }

    return render(request, 'artist/artist_list.html', context)

