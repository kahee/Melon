from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from config.settings import YOUTUBE_API_KEY


def video_list(request, name):
    """
    param에 가수 이름도 받아야 함
    :param request:
    :return:
    """
    key = YOUTUBE_API_KEY
    url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'key': key,
        'part': 'snippet',
        'q': name,
    }
