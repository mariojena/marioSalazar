from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>/", views.page, name="page"),
    path("new/", views.new, name="new"),
    path("edit/", views.edit, name="edit"),
    path("search/", views.search, name="search"),
    path("rand/", views.rand, name="rand"),
]
