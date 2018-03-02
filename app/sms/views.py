from urllib import request

from django.shortcuts import render, redirect

# Create your views here.
from .sms_test import send_massage


def send_sms(request):
    if request.method == 'POST':
        phonenum = request.POST['phonenum']
        message = request.POST['message']
        send_massage(phonenum, message)
        # 메시지 전송 함수 실행
        return redirect('index')

    else:
        return render(request, 'sms/send.html')
