import requests
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from artist.models import Artist
from config.settings import YOUTUBE_API_KEY
from video.models import Video


def video_add(request, artist_pk):
    """
    param에 가수 이름도 받아야 함
    :param request:
    :return:
    """
#     if request.method == 'POST':
#         artist = Artist.objects.get(pk=artist_pk)
# 1
#         key = YOUTUBE_API_KEY
#         url = 'https://www.googleapis.com/youtube/v3/search'
#         params = {
#             'key': key,
#             'part': 'snippet',
#             'q': artist.name,
#         }
#         response = requests.get(url, params)
#         response_dict = response.json()
#
#         video_lists = list()
#
#         for item in response_dict['items']:
#             video_id = item['id']['videoId']
#             title = item['snippet']['title']
#             img_url = item['snippet']['thumbnails']['medium']['url']
#
#             video_url = 'https://www.youtube.com/watch'
#             params = {
#                 'v': video_id,
#             }
#
#             href = requests.get(video_url, params).url
#
#             video_lists.append({
#                 'video_id': video_id,
#                 'title': title,
#                 'img_url': img_url,
#                 'name': artist.name,
#                 'href': href,
#             })
#
#         video, _ = Video.objects.update_or_create(
#             video_id=video_id,
#             title=title,
#             img_url=img_url,
#         )
#         video.artists.add(artist)
#
#         next_path = request.POST.get('next-path')
#         return redirect(next_path)
    pass