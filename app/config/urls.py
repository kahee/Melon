"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from config import views
from members.views import login_view, logout_view, signup_view, facebook_login

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.index, name='index'),
    path('', include('members.urls.views')),

    path('artist/', include('artist.urls.views')),
    path('album/', include('album.urls')),
    path('email/', include('email_send.urls')),
    path('sms/', include('sms.urls')),
    path('song/', include('song.urls')),
    path('video/', include('video.urls')),

    path('api/artist/', include('artist.urls.apis')),
    path('api/members/', include('members.urls.apis')),

]

# setting.MEDIA_URL ('/media/')로 시작하는 요청은
#  document_root인  settings.MEDIA_ROOT폴더(ROOT_DIR/.media)에서 파일을 찾아 리턴
#  개발 환경에서만 돌아가는 img
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
