from django.contrib.auth import logout
from django.shortcuts import redirect

__all__ = (
    'logout_view',
)
def logout_view(request):
    # /logout/
    #  GET/POST요청 둘다 상관없음
    logout(request)
    return redirect('index')
