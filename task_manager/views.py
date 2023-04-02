from django.shortcuts import render

from task_manager.models import Project, Task, Post, Commentary


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
