from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect

# user모델 클래스가져올때는 꼭 이렇게 할 것
User = get_user_model()

# Create your views here.
from members.models import User


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


def logout_view(request):
    # /logout/
    #  GET/POST요청 둘다 상관없음
    logout(request)
    return redirect('index')


def signup_view(request):
    # /signup/
    # username, password , password2가 전달되었다는 가정
    # username이 중복되는지 검사, 존재하지 않으면 유저 생성후 index로 이동
    # 이외의 경우, 다시 회원가입화면으로

    context = {
        'errors': []
    }

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        is_valid = True
        if User.objects.filter(username=username).exists():
            context['errors'].append('Username already exists')
            is_valid = False
        if password != password2:
            context['errors'].append('Password and Password2 is not equal')
            is_valid = False

        if is_valid:
            User.objects.create(username=username, password=password)
            return render(request, 'index.html')

    return render(request, 'members/signup.html', context)
