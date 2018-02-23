from django import forms

__all__ = (
    'SignupForm'
)


class SignupForm(forms.Form):
    username = forms.CharField(
        label="아이디",
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
