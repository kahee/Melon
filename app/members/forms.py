from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

__all__ = (
    'SignupForm'
)
User = get_user_model()


class SignupForm(forms.Form):
    username = forms.CharField(
        help_text='100 characters max.',
        label="아이디",
        # required= false 경우 빈칸을 submit할 수 있음
    )
    # widget은 CharField를 사용한다 했을 때 좀더 상세한 조건 넣어주기 위해
    password = forms.CharField(
        label="비밀번호",
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label="비밀번호확인",
        widget=forms.PasswordInput,
    )

    #  커스텀 메소드
    def clean_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists():
            raise ValidationError('이미 사용중인 아이디가 있습니다.')
        return data

    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']

        if password != password2:
            raise ValidationError('비밀번호가 일치하지 않습니다.')
        return password
