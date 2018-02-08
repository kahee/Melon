from . import views
from django.urls import path

urlpatterns = [
    path('song/', views.song_list, name='song-list')
]
