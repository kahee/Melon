from django.urls import path

from . import views

app_name = 'artist'
urlpatterns = [
    path('artist/', views.artist_list, name='artist-list'),
]
