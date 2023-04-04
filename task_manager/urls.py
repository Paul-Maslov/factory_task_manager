from django.urls import path, include

from task_manager.views import (
    index, about,
    PostListView, PostDetailView,
    CommentaryCreateView,
    EmployeeListView, EmployeeDetailView,
)

urlpatterns = [
    path("", index, name="index"),
    path("about/", about, name="about"),
    path("post/", PostListView.as_view(), name="post-list"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path(
        "post/<int:pk>/comment/",
        CommentaryCreateView.as_view(),
        name="post-create-comment"
    ),
    path("employees/", EmployeeListView.as_view(), name="employee-list"),
    path(
        "employees/<int:pk>/",
        EmployeeDetailView.as_view(),
        name="employee-detail"
    ),

]

app_name = "task_manager"
