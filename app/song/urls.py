from . import views
from django.urls import path

app_name = 'song'
urlpatterns = [
    path('', views.song_list, name='song-list'),
    path('search/', views.song_serarch, name='song-search')
]
