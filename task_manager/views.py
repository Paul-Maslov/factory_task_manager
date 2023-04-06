from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic

from task_manager.forms import CommentaryCreateForm
from task_manager.models import (
    Project, Task, Post, Commentary,
    Employee,
)


def index(request):
    """View function for the home page of the site."""

    num_projects = Project.objects.count()
    num_tasks = Task.objects.count()
    num_posts = Post.objects.count()
    num_commentaries = Commentary.objects.count()

    context = {
        "num_projects": num_projects,
        "num_tasks": num_tasks,
        "num_posts": num_posts,
        "num_commentaries": num_commentaries,
    }

    return render(request, "task_manager/index.html", context=context)


def about(request):
    return render(request, "task_manager/about.html")


class EmployeeListView(LoginRequiredMixin, generic.ListView):
    model = Employee
    paginate_by = 5
    queryset = Employee.objects.prefetch_related("task", "teams").order_by("last_name")


class EmployeeDetailView(LoginRequiredMixin, generic.DetailView):
    model = Employee


class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    paginate_by = 5
    queryset = Project.objects.select_related("project_type", "owner").prefetch_related(
       "team",
       "task",
    ).order_by("deadline")


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = Project
    fields = "__all__"
    success_url = reverse_lazy("task_manager:project-list")


class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Project
    fields = "__all__"
    success_url = reverse_lazy("task_manager:project-list")


class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Project
    template_name = "task_manager/project_confirm_delete.html"
    success_url = reverse_lazy("task_manager:project-list")


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    context_object_name = "project_detail"
    model = Project
    queryset = Project.objects.select_related(
        "owner"
    ).prefetch_related(
        "task"
    )


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 5
    queryset = Task.objects.select_related(
        "project"
    ).prefetch_related("assignees").order_by("deadline")


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    template_name = "task_manager/task_confirm_delete.html"
    success_url = reverse_lazy("task_manager:task-list")


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    context_object_name = "task_detail"
    model = Task
    queryset = Task.objects.select_related(
        "project"
    ).prefetch_related("post__owner")


class PostListView(LoginRequiredMixin, generic.ListView):
    model = Post
    queryset = Post.objects.select_related(
        "owner"
    ).prefetch_related(
        "commentaries"
    ).order_by("created_time")
    paginate_by = 5


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = "__all__"
    success_url = reverse_lazy("task_manager:post-list")


class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    fields = "__all__"
    success_url = reverse_lazy("task_manager:post-list")


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    template_name = "task_manager/post_confirm_delete.html"
    success_url = reverse_lazy("task_manager:post-list")


class PostDetailView(LoginRequiredMixin, generic.DetailView):
    context_object_name = "post_detail"
    model = Post
    queryset = Post.objects.prefetch_related(
        "task__assignees__task"
    ).prefetch_related(
        "commentaries"
    ).select_related(
        "owner"
    ).order_by("created_time")


class CommentaryCreateView(LoginRequiredMixin, generic.CreateView):

    def post(self, request, *args, **kwargs):
        post_id = kwargs["pk"]
        post_url = reverse("task_manager:post-detail", kwargs={"pk": post_id})
        form = CommentaryCreateForm(request.POST)

        if form.is_valid():
            content = form.cleaned_data["content"]

            if post_id and content:
                form.instance.user_id = self.request.user.pk
                form.instance.post_id = post_id
                self.success_url = post_url
                return super().form_valid(form)

        return HttpResponseRedirect(post_url)
