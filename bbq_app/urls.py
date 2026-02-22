from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

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
    path("events/<int:event_id>/delete/", views.event_delete, name="event_delete"),
    
]

