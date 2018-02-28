from datetime import datetime

from django.conf import settings
from django.db import models
from .artist import Artist

__all__ = (
    'ArtistLike',
)


class ArtistLike(models.Model):
    # Artist와 User(members.User)와의 관계를 나타내주는
    artist = models.ForeignKey(
        Artist,
        related_name='like_user_info_list',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='like_artist_info_list',
        on_delete=models.CASCADE,
    )
    created_date = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        # 같은 유저가 같은 아티스트 좋아요 누르는게 중복 되지 않게
        unique_together = (
            ('artist', 'user'),
        )

    def __str__(self):
        return 'ArtistLike (User:{user}, Artist:{artist}, Created:{created})'.format(
            artist=self.artist,
            user=self.user.username,
            created=datetime.strftime(self.created_date, '%Y.%m.%d'),
        )
