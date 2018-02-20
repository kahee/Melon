from django.contrib import admin

# Register your models here.
from song.models import Song

admin.site.register(Song)