from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=75, null=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Employee(AbstractUser):
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
    is_completed = models.BooleanField()
    owner = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
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
        return f"{self.name} ({self.owner.last_name})"


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
    is_completed = models.BooleanField()
    priority = models.CharField(
        max_length=1,
        choices=PRIORITY_CHOICES,
        default="B"
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    assignees = models.ManyToManyField(Employee, related_name="tasks")

    class Meta:
        ordering = ["deadline", "priority"]


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
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
