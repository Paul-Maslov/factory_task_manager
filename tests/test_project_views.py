from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from django.urls import reverse

from task_manager.models import (
    Position, Team,
    ProjectType, Project,
)

PROJECT_URL = reverse("task_manager:project-list")
PAGINATION = 1


class PublicProjectTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_list_login_required(self):
        res = self.client.get(PROJECT_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateProjectTests(TestCase):
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

    def test_project_list_response_with_correct_template(self):
        response = self.client.get(PROJECT_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "task_manager/project_list.html")

    def test_project_search_form(self):
        response = self.client.get(PROJECT_URL + "?name=find")

        self.assertContains(response, "find")
        self.assertNotContains(response, "moder")
        self.assertTemplateUsed(response, "task_manager/project_list.html")

    def test_project_list_paginate_correctly(self):
        pr_name = "Develop model Atlant"
        self.project = Project.objects.create(
            name=pr_name,
            is_completed=False,
            owner=self.employee,
            team=self.team,
            project_type=self.project_type
        )
        response = self.client.get(PROJECT_URL)

        self.assertEqual(len(response.context["project_list"]), PAGINATION)

    def test_project_detail_response_with_correct_template(self):
        pr_name = "Develop model Atlant"
        self.project = Project.objects.create(
            name=pr_name,
            is_completed=False,
            owner=self.employee,
            team=self.team,
            project_type=self.project_type
        )
        response = self.client.get(reverse("task_manager:project-detail", args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "task_manager/project_detail.html")





