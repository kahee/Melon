from django.shortcuts import redirect

from ...models import Song

__all__ = (
    'song_like',
)


def song_like(request, song_pk):
    if request.method == 'POST':
        song = Song.objects.get(pk=song_pk)
        song.toggle_like_user(request.user)
        next_path = request.POST.get('next-path', 'song:song-list')
        return redirect(next_path)
