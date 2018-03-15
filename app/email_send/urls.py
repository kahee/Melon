from . import views
from django.urls import path

app_name = 'email_send'
urlpatterns = [
    path('send/', views.email_send, name='email-send'),
]
