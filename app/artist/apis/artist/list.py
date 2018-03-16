import json

from django.http import JsonResponse, HttpResponse
from artist.models import Artist

__all__ = (
    'artist_list',
)


def artist_list(request):
    """
    data: {
        'artists':{
        {
            'melon_id':.....
            'name':...
        }
    }
    :param request:
    :return:
    """

    # localhost:8000/api/artist/

    # for artist in artists:
    #     artist_data = {
    #         'melon_id': artist.melon_id,
    #         'name': artist.name
    #     }
    #     artist_data_list.append(artist_data)
    #
    # data = {
    #     'artists':
    #         [
    #             {
    #                 'melon_id': artist.melon_id,
    #                 'name': artist.name,
    #                 'img_profile': artist.img_profile.url if artist.img_profile else None,
    #             }
    #             for artist in artists],
    # }

    artists = Artist.objects.all()

    data = {
        'artists': [artist.to_json() for artist in artists]
    }

    return JsonResponse(data)
    # return HttpResponse(json.dumps(data), content_type='application/json')

# /artist/          -> artist.urls.views
# /api/artists/     -> artist.urls.apis

# /album/           -> album.urls.views
# /api/album/       -> album.urls.apis
