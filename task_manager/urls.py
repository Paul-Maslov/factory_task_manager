from django.urls import path, include

from task_manager.views import (
    index, about,
    PostListView, PostDetailView,
    CommentaryCreateView,
)

urlpatterns = [
    path("", index, name="index"),
    path("about/", about, name="about"),
    path("post/", PostListView.as_view(), name="post"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path(
        "post/<int:pk>/comment/",
        CommentaryCreateView.as_view(),
        name="post-create-comment"
    ),
]

app_name = "task_manager"
