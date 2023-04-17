from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from meta.models import ModelMeta


class Position(models.Model):
    name = models.CharField(max_length=75, null=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Employee(AbstractUser, ModelMeta):
    photo = models.ImageField(upload_to="media/foto_users/", blank=True)
    position = models.ForeignKey(
        Position,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="employees"
    )

    class Meta:
        ordering = ["username"]
        verbose_name = "employee"
        verbose_name_plural = "employees"

    _metadata = {
           'photo': 'get_meta_photo',
    }

    def get_meta_image(self):
        if self.photo:
            return self.photo.url

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self) -> str:
        return reverse("task_manager:employee-detail", kwargs={"pk": self.pk})


class Team(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    employees = models.ManyToManyField(Employee, related_name="teams")

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class ProjectType(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(null=True, blank=True)
    fact_date = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField()
    owner = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="project",
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
    )
    project_type = models.ForeignKey(
        ProjectType,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ["deadline"]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if self.fact_date:
            self.is_completed = True
        super(Project, self).save(*args, **kwargs)


class Task(models.Model):
    PRIORITY_CHOICES = (
        ("A", "Urgent"),
        ("B", "No_delay"),
        ("C", "Need"),
    )
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(null=True, blank=True)
    fact_date = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField()
    priority = models.CharField(
        max_length=1,
        choices=PRIORITY_CHOICES,
        default="B"
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="task"
    )
    assignees = models.ManyToManyField(Employee, related_name="task")

    class Meta:
        ordering = ["deadline", "priority"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.fact_date:
            self.is_completed = True
        super(Task, self).save(*args, **kwargs)


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
        related_name="post"
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="post",
    )

    class Meta:
        ordering = ["created_time"]

    def __str__(self) -> str:
        return self.title


class Commentary(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        name="user",
        related_name="commentaries",
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        name="post",
        related_name="commentaries",
    )
    content = models.TextField(null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_time"]
