""" содержит код для настройки URL-адресов в Django. 
Он определяет маршруты для различных представлений (views),
связанных с управлением контентом блога."""
from django.urls import path

from . import views

app_name = 'blog'#пространство имен для URL адресов

urlpatterns = [
    path(
        '',
        views.IndexListView.as_view(),#главная страница
        name='index'
    ),
    path(
        'posts/<int:post_id>/',
        views.PostDetailView.as_view(),#конкретный пост
        name='post_detail'
    ),
    path(
        'posts/<int:post_id>/edit/',
        views.PostUpdateView.as_view(),#редактирование поста
        name='edit_post'
    ),
    path(
        'posts/<int:post_id>/delete/',
        views.PostDeleteView.as_view(),#удаление поста
        name='delete_post'
    ),
    path(
        'posts/<int:post_id>/comment/',
        views.CommentCreateView.as_view(),#добавление комментария к публикации
        name='add_comment'
    ),
    path(
        'posts/create/',
        views.CreatePostView.as_view(),#создание нового поста
        name='create_post'
    ),
    path(
        'posts/<int:post_id>/edit_comment/<int:comment_id>/',
        views.CommentUpdateView.as_view(),
        name='edit_comment'
    ),
    path(
        'posts/<int:post_id>/delete_comment/<int:comment_id>/',
        views.CommentDeleteView.as_view(),
        name='delete_comment'
    ),
    path(
        'category/<slug:category_slug>/',
        views.CategoryDetailView.as_view(),
        name='category_posts'
    ),
    path(
        'profile/<slug:username>/',
        views.ProfileView.as_view(),
        name='profile'
    ),
    path(
        'profile/<slug:username>/edit/',
        views.ProfileEditView.as_view(),
        name='edit_profile'
    ),
]
