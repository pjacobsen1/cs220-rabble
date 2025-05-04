from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("profile", views.profile, name="profile"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("!<slug:subrabble_name>/", views.subrabble_detail, name="subrabble-detail"),
    path("!<slug:subrabble_name>/<int:pk>/", views.post_detail, name="post-detail"),
    path("!<slug:subrabble_name>/new", views.post_create, name="post-create"),
    path("!<slug:subrabble_name>/<int:pk>/edit", views.post_edit, name="post-edit")
]
