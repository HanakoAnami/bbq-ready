from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.portfolio, name="portfolio"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("signup/", views.signup, name="signup"),
    path("home/", views.home, name="home"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("events/new/", views.event_create, name="event_create"),
    path("events/create/", views.event_create, name="event_create"),
    path("events/<int:event_id>/items/", views.item_edit, name="item_edit"),
    path("events/<int:event_id>/duplicate/", views.event_duplicate, name="event_duplicate"),
    path("events/", views.event_list, name="event_list"),
    path("events/<int:event_id>/edit/", views.event_edit, name="event_edit"),
    path("events/<int:event_id>/delete/", views.event_delete, name="event_delete"),
    path("events/<int:event_id>/participants/", views.event_participants, name="event_participants"),
    path("mypage/", views.mypage, name="mypage"),
    path("mypage/name/", views.mypage_name, name="mypage_name"),
    path("mypage/email/", views.mypage_email, name="mypage_email"),
    path("mypage/password/", auth_views.PasswordChangeView.as_view(template_name="bbq_app/mypage_password.html",success_url=reverse_lazy("mypage")), name="mypage_password"),
    path("items/templates/", views.bbqitem_list_create, name="bbq_list_create"),
]

