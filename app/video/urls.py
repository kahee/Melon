from django.urls import path
from . import views

app_name = 'video'
urlpatterns = [
      path('<int:artist_pk>/add/', views.video_add, name='video-add'),
]