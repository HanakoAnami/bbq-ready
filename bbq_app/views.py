from django.shortcuts import render
from django.contrib.auth.views import LoginView


def portfolio(request):# ポートフォリオトップページ
    return render(request, 'bbq_app/portfolio.html')

def index(request):# ログイン後の画面用
    return render(request, 'bbq_app/index.html')

class UserLoginView(LoginView):
    template_name = 'bbq_app/login.html'
