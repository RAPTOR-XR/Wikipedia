from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.new_entry, name="entry"),
    path("search", views.search, name="search"),
    path("create", views.create_new, name="create"),
    path("edit/<str:title>", views.edit_page, name="edit"),
    path("wiki/", views.random, name="random")
]
