from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect

__all__ = (
    'login_view',
)



def login_view(request):
    # POST요청일때는
    # authentication -> login 후 'index"로 redirect
    #
    # GET요청일때는
    # members/login.html 파일을 보여줌
    #   해당 파일의 form에는 username, password input 과 로그인 버튼있음
    #   form은 method POST로 다시 이 view로의 action 값을 가짐

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')

    return render(request, 'members/login_view.html')
