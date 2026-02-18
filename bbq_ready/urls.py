from django.contrib import admin
from django.urls import path
from bbq_app import views  # さっき書いたviewsを使えるように呼ぶ

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.portfolio, name='portfolio'),  # 何もなし('')の時はポートフォリオ
    path('home/', views.index, name='index'),      # 'home/' の時はメイン画面
]