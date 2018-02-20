from django.urls import path
from . import views

app_name = 'album'
urlpatterns = [
    path('album/', views.album_list, name='album-list'),
]
