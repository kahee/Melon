import requests
from django.contrib.auth import login, get_user_model
from django.http import HttpResponse
from django.shortcuts import redirect

User = get_user_model()

from config import settings

__all__ = (
    'facebook_login',
)


def facebook_login(request):
    # code로부터 AccessToken 가져오기
    client_id = settings.FACEBOOK_APP_ID
    client_secret = settings.FACEBOOK_SECRET_CODE
    # 페이스북 로그인 버튼을 누른 후, 사용자가 승인하면 redirect_url에 GET parameter로 'code'가 전송됨
    # 이 값과 client_id, secret을 사용해서 Facebook서버에서 access_token을 받아와야 함
    code = request.GET['code']
    # 이전에 페이스북 로그인 버튼을 눌렀을 때, 'code'를 다시 전달받은 redirect_url값으로 그대로 사용
    redirect_uri = 'http://localhost:8000/facebook-login/'

    # 아래 엔드포인트에 get요청을 보냄
    url = 'https://graph.facebook.com/v2.12/oauth/access_token'
    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'client_secret': client_secret,
        'code': code,
    }

    response = requests.get(url, params)
    # 전송받은 결과를 json형식의 텍스트,
    response_dict = response.json()

    for key, value in response_dict.items():
        print(f'{key}:{value}')

    # GraphAPI  me 엔드포인트에 GET요청 보내기
    # API url = 엔드포인트
    url = 'https://graph.facebook.com/v2.12/me'
    params = {
        'access_token': response_dict['access_token'],
        'fields': ','.join([
            'id',
            'name',
            'first_name',
            'last_name',
        ])
    }

    response = requests.get(url, params)
    response_dict = response.json()

    # 고유한 id는 아니고 애플리케이션에 따라 바뀌는 값
    facebook_id = response_dict['id']
    name = response_dict['name']
    first_name = response_dict['first_name']
    last_name = response_dict['last_name']
    # picture = response_dict['picture']['data']['url']

    if User.objects.filter(username=facebook_id):
        user = User.objects.get(username=facebook_id)
        login(request, user)
        return redirect('index')

    else:
        user = User.objects.create_user(
            username=facebook_id,
            first_name=first_name,
            last_name=last_name,
        )
        login(request, user)
        return redirect('index')

    return HttpResponse(str(response_dict))

# access_token:EAAE9ZCVbK44wBAA5qyAj7k2ehJQZAWULRcLa1L74jhkVmpzTqeoZAJFHZAhy8QiusDk1SLYvLXpUNJZA5HEYROpRap0cO76hcv23Nr4B3dSwbtAVQ8dJqDp0ClTvHA0PjZCw9bZCOVD4IQVjqZCgSpJw2gApHeGHnYQLztuiELqZBkQZDZD
# token_type:bearer
# expires_in:5181467
