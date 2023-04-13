from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.models import (
    Project, Team,
    ProjectType,
)


class ProjectFormTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Paul",
            password="user12345",
        )
        self.client.force_login(self.user)

        username = "test_user1"
        password = "user112345"
        self.employee = get_user_model().objects.create_user(
            username=username,
            password=password,
        )
        self.team = Team.objects.create(
            name="Developers"
        )
        self.project_type = ProjectType.objects.create(
            name="DEV"
        )

    def test_create_project(self):
        pr_name = "Develop model Atlant"
        response = self.client.post(
            reverse(
                "task_manager:project-create",
            ),
            {
                "name": pr_name,
                "description": "Use cheaper materials",
                "is_completed": "False",
                "owner": self.user.id,
                "team": self.team.id,
                "project_type": self.project_type.id
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Project.objects.get(id=1).name, "Develop model Atlant")

    def test_update_project(self):
        pr_name = "Develop model Atlant"
        project = Project.objects.create(
            name=pr_name,
            is_completed=False,
            owner=self.employee,
            team=self.team,
            project_type=self.project_type
        )
        response = self.client.post(
            reverse("task_manager:project-update", kwargs={"pk": project.id}),
            {
                "pk": project.id,
                "name": "Develop model AKVA",
                "is_completed": "False",
                "owner": self.employee.id,
                "team": self.team.id,
                "project_type": self.project_type.id
            },
        )
        Project.objects.get(id=project.id).refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Project.objects.get(id=project.id).name, "Develop model AKVA")

    def test_delete_project(self):
        pr_name = "Develop model Atlant"
        project = Project.objects.create(
            name=pr_name,
            is_completed=False,
            owner=self.employee,
            team=self.team,
            project_type=self.project_type
        )
        response = self.client.post(
            reverse("task_manager:project-delete", kwargs={"pk": project.id})
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Project.objects.filter(id=project.id).exists())
