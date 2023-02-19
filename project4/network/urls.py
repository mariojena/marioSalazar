
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.add_post, name="add_post"),
    path("user/<int:id>", views.page_user, name="page_user"),
    path("settings", views.settings, name="settings"),
    path("password_change", views.password_change, name="password_change"),
    path("following", views.following, name="following"),
    path("notifications", views.notifications, name="notifications"),
    path("search", views.search, name="search"),


    #API routes
    path("comment", views.comment, name="comment"),
    path("like_post", views.like_post, name="like_post"),
    path("like_comment", views.like_comment, name="like_comment"),
    path("edit_getpost", views.edit_getpost, name="edit_getpost"),
    path("edit_post", views.edit_post, name="edit_post"),
    path("accept_request", views.accept_request, name="accept_request"),
    path("delete_request", views.delete_request, name="delete_request"),
    path("send_request", views.send_request, name="send_request"),
    path("delete_element", views.delete_element, name="delete_element"),
]
