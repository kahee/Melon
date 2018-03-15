from django.core.mail import EmailMessage, send_mail
from django.shortcuts import render, redirect

# Create your views here.
from email_send.form import EmailForm


def email_send(request):
    context = dict()

    if request.method == 'POST':
        form = EmailForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            # 제목
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            send_mail(subject, message, 'yuygh131@gmail.com', [email])

            return redirect('index')

    else:
        form = EmailForm()

    context['email_form'] = form

    return render(request, 'email/email_send.html', context)
