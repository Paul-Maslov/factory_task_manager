from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic

from task_manager.forms import (
    CommentaryCreateForm, EmployeeCreationForm,
    EmployeeSearchForm, ProjectSearchForm,
    TaskSearchForm, PostSearchForm,
    TaskForm, ProjectForm,
)
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
    queryset = Employee.objects.prefetch_related(
        "task", "teams"
    ).order_by("last_name")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EmployeeListView, self).get_context_data(**kwargs)

        username = self.request.GET.get("username", "")

        context["search_form"] = EmployeeSearchForm(
            initial={"username": username}
        )

        return context

    def get_queryset(self):
        queryset = Employee.objects.all()
        form = EmployeeSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )

        return queryset


class EmployeeCreateView(LoginRequiredMixin, generic.CreateView):
    model = Employee
    form_class = EmployeeCreationForm


class EmployeeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Employee
    fields = "__all__"
    success_url = reverse_lazy("task_manager:employee-list")


class EmployeeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Employee
    success_url = reverse_lazy("task_manager:employee-list")


class EmployeeDetailView(LoginRequiredMixin, generic.DetailView):
    model = Employee

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EmployeeDetailView, self).get_context_data(**kwargs)
        context['meta'] = self.get_object().as_meta(self.request)
        return context


class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    paginate_by = 5
    queryset = Project.objects.select_related(
        "project_type",
        "owner"
    ).prefetch_related(
       "team",
       "task",
    ).order_by("deadline")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = ProjectSearchForm(
            initial={"name": name}
        )

        return context

    def get_queryset(self):
        queryset = Project.objects.all()
        form = ProjectSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )

        return queryset


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
    success_url = reverse_lazy("task_manager:project-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)

        fact_date = self.request.GET.get("fact_date", "")

        context["done_form"] = ProjectForm(
            initial={"fact_date": fact_date}
        )

        return context

    def post(self, request, *args, **kwargs):
        project_id = kwargs["pk"]
        post_url = reverse("task_manager:task-detail", kwargs={"pk": project_id})
        form = TaskForm(request.POST)

        if form.is_valid():
            content = form.cleaned_data["fact_date"]

            project = Project.objects.get(pk=project_id)
            project.fact_date = content
            project.save()

        return HttpResponseRedirect(post_url)


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 5
    queryset = Task.objects.select_related(
        "project"
    ).prefetch_related("assignees").order_by("deadline")
    success_url = reverse_lazy("task_manager:task-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = TaskSearchForm(
            initial={"name": name}
        )

        return context

    def get_queryset(self):
        queryset = Task.objects.all()
        form = TaskSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )

        return queryset


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
    success_url = reverse_lazy("task_manager:task-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)

        fact_date = self.request.GET.get("fact_date", "")

        context["done_form"] = TaskForm(
            initial={"fact_date": fact_date}
        )

        return context

    def post(self, request, *args, **kwargs):
        task_id = kwargs["pk"]
        post_url = reverse("task_manager:task-detail", kwargs={"pk": task_id})
        form = TaskForm(request.POST)

        if form.is_valid():
            content = form.cleaned_data["fact_date"]

            task = Task.objects.get(pk=task_id)
            task.fact_date = content
            task.save()

        return HttpResponseRedirect(post_url)


class PostListView(LoginRequiredMixin, generic.ListView):
    model = Post
    queryset = Post.objects.select_related(
        "owner"
    ).prefetch_related(
        "commentaries"
    ).order_by("created_time")
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)

        title = self.request.GET.get("name", "")

        context["search_form"] = PostSearchForm(
            initial={"title": title}
        )

        return context

    def get_queryset(self):
        queryset = Post.objects.all()
        form = PostSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                title__icontains=form.cleaned_data["title"]
            )

        return queryset


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
