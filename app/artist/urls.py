from django.urls import path

from . import views

app_name = 'artist'
urlpatterns = [
    path('', views.artist_list, name='artist-list'),
    path('add/', views.artist_create, name='artist-add'),
    path('search/melon/', views.artist_search_from_melon, name='artist-search-melon'),
]
