from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.views import View
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.core.mail import EmailMessage
from django.core.mail import get_connection
from django.core.mail.message import BadHeaderError
from django.http import HttpResponse


class CustomEmailMessage(EmailMessage):
    def message(self):
        msg = super().message()
        msg.set_charset('utf-8')
        msg.replace_header('Content-Type', 'text/plain; charset="utf-8"')
        return msg

def send_mail():
    subject = "unblock"
    message = "hi"
    from_email = 'from-user@mail.ru'
    to_email = "my-site@mail.ru"

    email = CustomEmailMessage(subject, message, from_email, [to_email])

    try:
        connection = get_connection()
        connection.send_messages([email])
    except BadHeaderError:
        return HttpResponse('Invalid header found.')

    return HttpResponse('Email sent successfully.')

def block_reset(request):
    send_mail()
    return render(request, 'block_reset.html')


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'


class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': CustomUserCreationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)
