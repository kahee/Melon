from django.contrib import admin

# Register your models here.
from .models import Artist, ArtistLike, ArtistYouTube

admin.site.register(Artist)
admin.site.register(ArtistLike)
admin.site.register(ArtistYouTube)
