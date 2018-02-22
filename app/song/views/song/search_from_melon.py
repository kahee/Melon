from django.shortcuts import render
from django.views.decorators.http import require_GET
from crawler.song_data import song_list_crawler

__all__ = [
    'song_search_from_melon',
]

# 405 오류
@require_GET
def song_search_from_melon(request):

    keyword = request.GET.get('keyword')

    result = song_list_crawler(keyword)

    context = {
        'result': result,
    }

    return render(request, 'song/song_search_from_melon.html', context)

