from django.shortcuts import render

def portfolio(request):# ポートフォリオトップページ
    return render(request, 'bbq_app/portfolio.html')

def index(request):# ログイン後の画面用
    return render(request, 'bbq_app/index.html')