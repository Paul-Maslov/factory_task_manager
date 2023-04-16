from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.models import (
    Team, ProjectType,
    Project, Task,
)


class TaskFormsTests(TestCase):
    def setUp(self):
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
        pr_name = "Develop model Atlant"
        self.project = Project.objects.create(
            name=pr_name,
            is_completed=False,
            owner=self.employee,
            team=self.team,
            project_type=self.project_type
        )

    def test_create_task(self):
        task_name = "Test create Task"
        response = self.client.post(
            reverse(
                "task_manager:task-create"
            ),
            {
                "name": task_name,
                "description": "Testing of creation task",
                "is_completed": "False",
                "priority": "A",
                "project": self.project.id,
                "assignees": [self.user.id, ]
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.get(id=1).name, "Test create Task")
        self.assertEqual(Task.objects.get(id=1).description, "Testing of creation task")
        self.assertEqual(Task.objects.get(id=1).priority, "A")
        self.assertEqual(Task.objects.get(id=1).project.name, "Develop model Atlant")

    def test_update_task(self):
        task_name = "Test create Task"
        task = Task.objects.create(
            name=task_name,
            description="Try to create Task",
            is_completed=False,
            project=self.project,
        )

        response = self.client.post(
            reverse(
                "task_manager:task-update",
                kwargs={"pk": task.id}
            ),
            {
                "pk": task.id,
                "name": "Test update Task",
                "description": "Try to update Task",
                "is_completed": "False",
                "priority": "B",
                "project": self.project.id,
                "assignees": self.user.id

            },
        )
        Task.objects.get(id=task.id).refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.get(id=task.id).name, "Test update Task")
        self.assertEqual(Task.objects.get(id=task.id).description, "Try to update Task")
        self.assertEqual(Task.objects.get(id=task.id).priority, "B")
        self.assertEqual(Task.objects.get(id=task.id).project.name, "Develop model Atlant")

    def test_delete_task(self):
        task_name = "Test delete Task"
        task = Task.objects.create(
            name=task_name,
            description="Try to delete Task",
            is_completed=False,
            project=self.project,
        )
        task.assignees.set([self.employee, ])
        response = self.client.post(
                reverse("task_manager:task-delete", kwargs={"pk": task.id})
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=task.id).exists())
