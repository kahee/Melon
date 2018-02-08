# from django.db import models
#
# # Create your tests here.
# from album.models import Album
# from artist.models import Artist
#
#
# class Song(models.Model):
#     song_title = models.CharField('곡명', max_length=100, )
#     # 가수 : 곡 = 1: N
#     artist = models.ForeignKey(
#         '가수명',
#         Artist,
#         on_delete=models.CASCADE,
#     )
#     album = models.ForeignKey(
#         '앨범명',
#         Album,
#         on_delete=models.CASCADE,
#     )
#     lyrics = models.TextField('가사', blank=True,)
#
