from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required


def portfolio(request):
    return render(request, 'bbq_app/portfolio.html')

@login_required
def home(request):# ログイン後の画面用
    return render(request, 'bbq_app/home.html')

class UserLoginView(LoginView):
    template_name = 'bbq_app/login.html'
