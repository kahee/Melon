from django.contrib import admin

# Register your models here.
from album.models import Album, AlbumLike

admin.site.register(Album)
admin.site.register(AlbumLike)