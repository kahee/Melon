from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # User클래스 정의
    # INstalled_Apps에 members applications 추가
    # AUTH_USER_MODEL  정의 (AppName.ModelClassName)
    # 모든 apllication들의 migrations폴더내의 Migration파일 전부 삭제
    # makemigrations -> migrate
    # 데이터베이스에 usr 생성됬는지 확인
    def toggle_like_artist(self, artist):
        like, like_created = self.like_artist_info_list.get_or_create(artist=artist)
        if not like_created:
            like.delete()
        return like_created

    def toggle_like_album(self, album):
        like, like_crated = self.like_album_info_list.get_or_create(album=album)
        if not like_crated:
            like.delete()
        return like_crated
