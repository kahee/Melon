from django.urls import path

from ..views import login_view, logout_view, signup_view, facebook_login

urlpatterns = (
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_view, name='signup'),
    path('facebook-login/', facebook_login, name='facebook-login'),
)