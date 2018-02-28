from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse

from artist.models import Artist, ArtistYouTube

__all__ = (
    'artist_add_youtube',
)


def artist_add_youtube(request, artist_pk):
    # artist_pk에 해당하는 Artist에게
    # request.POST로 전달된 youtube_id, title, url_thumbnail을 가지는
    # ArtistYouTube를  Artist의 youtube_videos에 추가

    artist = get_object_or_404(Artist, pk=artist_pk)

    if request.method == 'POST':
        youtube_id = request.POST['youtube_id']
        title = request.POST.get('title')
        url_thumbnail = request.POST.get('url_thumbnail')

        artist.youtube_videos.update_or_create(
            youtube_id=youtube_id,
            # title과 썸네일은 바뀔 수도 있으므로 update
            defaults={
                "title": title,
                "url_thumbnail": url_thumbnail,
            }
        )

        next_path = request.POST.get(
            'next-path',
            # reverse('artist:artist-detail', args=[artist_pk]))
            reverse('artist:artist-detail', kwargs={'artist_pk': artist_pk}))


        return redirect(next_path)
