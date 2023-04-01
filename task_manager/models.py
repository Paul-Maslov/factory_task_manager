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


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
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
