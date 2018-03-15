from django.shortcuts import render, redirect

from ...models import Album

__all__ = (
    'album_like',
)


def album_like(request, album_pk):

    if request.method == 'POST':
        album = Album.objects.get(pk=album_pk)
        album.toggle_like_user(request.user)
        next_path = request.POST.get('next-path', 'album:album-list.py')
    return redirect(next_path)
