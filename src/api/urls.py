from django.urls import path
from . import views

urlpatterns = [
    path('subrabbles/', views.subrabble_list, name='subrabble-list'),
    path('subrabbles/!<str:subrabble_name>/', views.get_subrabble, name='get-subrabble'),
    path('subrabbles/!<str:subrabble_name>/posts/', views.subrabble_posts, name='subrabble-posts'),
    path('subrabbles/!<str:subrabble_name>/posts/<int:pk>/', views.get_post, name='get-post'),
    path('subrabbles/!<str:subrabble_name>/posts/<int:pk>/likes/', views.change_like, name='change-like'),
]