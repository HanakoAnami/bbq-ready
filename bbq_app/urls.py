from django.urls import path
from . import views

urlpatterns = [
    path('', views.portfolio, name='portfolio'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('home/', views.home, name='home'),
]
