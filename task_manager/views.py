from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
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
    queryset = Employee.objects.prefetch_related("tasks", "teams").order_by("last_name")


class EmployeeDetailView(LoginRequiredMixin, generic.DetailView):
    model = Employee


class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    paginate_by = 5
    queryset = Project.objects.select_related("project_type", "owner").prefetch_related(
       "team",
       "task_set",
    ).order_by("deadline")


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    context_object_name = "project_detail"
    model = Project
    queryset = Project.objects.select_related(
        "owner"
    ).prefetch_related(
        "task_set"
    ).order_by("deadline")


class PostListView(LoginRequiredMixin, generic.ListView):
    model = Post
    queryset = Post.objects.select_related(
        "owner"
    ).prefetch_related(
        "commentaries"
    ).order_by("created_time")
    paginate_by = 5


class PostDetailView(LoginRequiredMixin, generic.DetailView):
    context_object_name = "post_detail"
    model = Post
    queryset = Post.objects.prefetch_related(
        "task__assignees__tasks"
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
