from django.shortcuts import render, get_object_or_404

from ...models import Artist

__all__ = (
    'artist_detail',
)


def artist_detail(request, artist_pk):
    # artist_pk에 해당하는 Artist정보 보여주기
    # Template: artist/artist_detail.html

    artist = get_object_or_404(Artist, pk=artist_pk)

    context = {
        'artist': artist,
    }

    return render(request, 'artist/artist_detail.html', context)
