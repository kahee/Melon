from django.urls import path, include
from django.contrib import admin

from ..views import index

urlpatterns = (
    path('admin/', admin.site.urls),

    path('', index, name='index'),
    path('', include('members.urls.views')),

    path('artist/', include('artist.urls.views')),
    path('album/', include('album.urls')),
    path('email/', include('email_send.urls')),
    path('sms/', include('sms.urls')),
    path('song/', include('song.urls')),
    path('video/', include('video.urls')),

)