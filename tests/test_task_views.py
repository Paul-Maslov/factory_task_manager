from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from django.urls import reverse

from task_manager.models import (
    Position, Team, ProjectType,
    Project, Task
)

TASK_URL = reverse("task_manager:task-list")
PAGINATION = 1


class PublicTaskTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_list_login_required(self):
        res = self.client.get(TASK_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivatePostTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="user12345",
        )
        self.client.force_login(self.user)
        self.position = Position.objects.create(
            name="director"
        )
        username = "test_user1"
        password = "user112345"
        self.employee = get_user_model().objects.create_user(
            username=username,
            password=password,
            position=self.position
        )
        self.team = Team.objects.create(
            name="Developers"
        )
        self.project_type = ProjectType.objects.create(
            name="DEV"
        )
        pr_name = "Develop model Atlant"
        self.project = Project.objects.create(
            name=pr_name,
            is_completed=False,
            owner=self.employee,
            team=self.team,
            project_type=self.project_type
        )

    def test_task_list_response_with_correct_template(self):
        response = self.client.get(TASK_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "task_manager/task_list.html")

    def test_search_task_form(self):
        response = self.client.get(TASK_URL + "?name=develop")

        self.assertContains(response, "develop")
        self.assertNotContains(response, "modernization")
        self.assertTemplateUsed(response, "task_manager/task_list.html")

    def test_task_list_paginated_correctly(self):
        task_name = "Design the sofa seat"
        self.task = Task.objects.create(
            name=task_name,
            is_completed=False,
            project=self.project
        )
        response = self.client.get(TASK_URL)
        self.assertEqual(len(response.context["task_list"]), PAGINATION)

    def test_task_detail_response_with_correct_template(self):
        task_name = "Design the sofa seat"
        self.task = Task.objects.create(
            name=task_name,
            is_completed=False,
            project=self.project
        )
        response = self.client.get(reverse("task_manager:task-detail", args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "task_manager/task_detail.html")
