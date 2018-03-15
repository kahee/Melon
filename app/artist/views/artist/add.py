import datetime
from django.shortcuts import redirect, render
from ...forms import ArtistForm



__all__ = (
    'artist_create',
)


def artist_create(request):
    if request.method == 'POST':

        # 이미지 파일의 경우, POST에 같이 오지 않음 -> request.FIELS
        form = ArtistForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('artist:artist-list.py')

    else:
        form = ArtistForm()

    context = {
        'artist_form': form,
    }

    return render(request, 'artist/artist_create.html', context)
