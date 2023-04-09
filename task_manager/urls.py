from django.urls import path

from task_manager.views import (
    index, about,
    PostListView, PostDetailView,
    PostCreateView, PostUpdateView, PostDeleteView,
    CommentaryCreateView,
    EmployeeListView, EmployeeDetailView,
    EmployeeCreateView, EmployeeUpdateView, EmployeeDeleteView,
    ProjectListView, ProjectDetailView,
    ProjectCreateView, ProjectUpdateView, ProjectDeleteView,
    TaskListView, TaskDetailView,
    TaskCreateView, TaskUpdateView, TaskDeleteView,
)

urlpatterns = [
    path("", index, name="index"),
    path("about/", about, name="about"),
    path("post/", PostListView.as_view(), name="post-list"),
    path("post/create/", PostCreateView.as_view(), name="post-create"),
    path(
        "post/<int:pk>/update/",
        PostUpdateView.as_view(),
        name="post-update"
    ),
    path(
        "post/<int:pk>/delete/",
        PostDeleteView.as_view(),
        name="post-delete"
    ),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path(
        "post/<int:pk>/comment/",
        CommentaryCreateView.as_view(),
        name="post-create-comment"
    ),
    path("employees/", EmployeeListView.as_view(), name="employee-list"),
    path(
        "employees/create/",
        EmployeeCreateView.as_view(),
        name="employee-create"
    ),
    path(
        "employees/<int:pk>/update/",
        EmployeeUpdateView.as_view(),
        name="employee-update"
    ),
    path(
        "employees/<int:pk>/delete/",
        EmployeeDeleteView.as_view(),
        name="employee-delete"
    ),
    path(
        "employees/<int:pk>/",
        EmployeeDetailView.as_view(),
        name="employee-detail"
    ),
    path("projects/", ProjectListView.as_view(), name="project-list"),
    path(
        "projects/create/",
        ProjectCreateView.as_view(),
        name="project-create"
    ),
    path(
        "projects/<int:pk>/update/",
        ProjectUpdateView.as_view(),
        name="project-update"
    ),
    path(
        "projects/<int:pk>/delete/",
        ProjectDeleteView.as_view(),
        name="project-delete"
    ),
    path(
        "projects/<int:pk>/",
        ProjectDetailView.as_view(),
        name="project-detail"
    ),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/create", TaskCreateView.as_view(), name="task-create"),
    path(
        "tasks/<int:pk>/update",
        TaskUpdateView.as_view(),
        name="task-update"
    ),
    path(
        "tasks/<int:pk>/delete",
        TaskDeleteView.as_view(),
        name="task-delete"
    ),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),

]

app_name = "task_manager"
