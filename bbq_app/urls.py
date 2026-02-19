from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.portfolio, name='portfolio'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
