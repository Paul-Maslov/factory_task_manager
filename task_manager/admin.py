from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from task_manager.models import (
    Post, Commentary, Employee,
    Position, Team, ProjectType,
    Project, Task
)

admin.site.unregister(Group)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["owner", "title", "content", "created_time"]
    list_filter = ["created_time", "owner"]
    search_fields = ["title"]


@admin.register(Commentary)
class CommentaryAdmin(admin.ModelAdmin):
    list_display = ["user", "post", "content", "created_time"]
    list_filter = ["post", "created_time"]
    search_fields = ["post"]


@admin.register(Employee)
class EmployeeAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {"fields": ("position", "photo")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional info", {"fields": (
            "first_name", "last_name", "position", "photo",
        )}),
    )


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(ProjectType)
class ProjectTypeAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        "owner",
        "name",
        "description",
        "deadline",
        "team",
        "is_completed",
    ]
    list_filter = [
        "deadline",
        "team",
        "is_completed",
    ]
    search_fields = [
        "owner",
        "name",
    ]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "project",
        "name",
        "description",
        "deadline",
        "priority",
        "is_completed",
    ]
    list_filter = [
        "deadline",
        "project",
        "priority",
        "is_completed",
    ]
    search_fields = [
        "name",
    ]
