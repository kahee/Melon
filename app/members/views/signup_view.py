from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
# user모델 클래스가져올때는 꼭 이렇게 할 것
from members.forms import SignupForm
User = get_user_model()
# Create your views here.
from members.models import User


__all__ = (
    'signup_view',
)

def signup_view(request):
    # /signup/
    # username, password , password2가 전달되었다는 가정
    # username이 중복되는지 검사, 존재하지 않으면 유저 생성후 index로 이동
    # 이외의 경우, 다시 회원가입화면으로
    context = {
        'error': list()
    }

    if request.method == 'POST':
        # form 자체에 데이터가 들어감
        form = SignupForm(request.POST)

        # 커스텀 메소드랑 연결되는 부분 공부할 것
        # 유효성 검사가 패스된 경우 입력된 데이터를 cleaned_data에서 사용가능
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            User.objects.create_user(username=username, password=password)
            return redirect('index')

    else:
        # form 빈 폼
        form = SignupForm()

    # {% extends parents %}
    # context[parents] = get.tamplates()

    context['signup_form'] = form

    return render(request, 'members/signup.html', context)
