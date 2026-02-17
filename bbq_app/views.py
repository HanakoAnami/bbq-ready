from django.http import HttpResponse

def index(request):
    return HttpResponse("はなこさんのBBQアプリ、準備開始！")