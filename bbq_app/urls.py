from django.urls import path
from . import views

urlpatterns = [
    path('', views.portfolio, name='portfolio'),
    path('home/', views.index, name='index'),
    path('login/', views.UserLoginView.as_view(), name='login'),
]
