from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("<str:memo_id>/", views.saved, name="saved"),
    path("<str:memo_id>/r", views.read, name="read"),
    path("<str:memo_id>/edit", views.edit, name="edit"),
    path("<str:memo_id>/fork", views.fork_new_id, name="fork"),
]
# подключаем urls приложения