from django.contrib.auth import get_user_model
from django.test import TestCase

from task_manager.models import (
    Position, ProjectType,
    Team, Project, Task, Employee,
)


class ModelTests(TestCase):
    def test_position_str(self) -> None:
        position_ = Position.objects.create(
            name="director"
        )

        self.assertEqual(str(position_), position_.name)

    def test_project_type_str(self) -> None:
        project_type_ = ProjectType.objects.create(
            name="Development"
        )

        self.assertEqual(str(project_type_), project_type_.name)

    def test_employee_str(self) -> None:
        employee = get_user_model().objects.create_user(
            username="test_user",
            password="user12345",
            first_name="Ivan",
            last_name="Derevyanko",
        )

        self.assertEqual(str(employee), f"{employee.first_name} {employee.last_name}")

    def test_employee_create_with_position(self) -> None:
        position = Position.objects.create(
            name="director"
        )
        username = "test_user"
        password = "user12345"
        employee = get_user_model().objects.create_user(
            username=username,
            password=password,
            position=position
        )

        self.assertEqual(employee.username, username)
        self.assertTrue(employee.check_password(password))
        self.assertEqual(employee.position, position)

    def test_project_create_with_all_elements(self) -> None:
        position = Position.objects.create(
            name="director"
        )
        username = "test_user"
        password = "user12345"
        employee = get_user_model().objects.create_user(
            username=username,
            password=password,
            position=position
        )
        team = Team.objects.create(
            name="Developers"
        )
        pr_type = ProjectType.objects.create(
            name="DEV"
        )
        pr_name = "Develop model Atlant"
        project = Project.objects.create(
            name=pr_name,
            is_completed=False,
            owner=employee,
            team=team,
            project_type=pr_type
        )

        self.assertEqual(project.name, pr_name)
        self.assertEqual(project.is_completed, False)
        self.assertEqual(project.owner, employee)
        self.assertEqual(project.team, team)
        self.assertEqual(project.project_type, pr_type)

    def test_task_create_with_all_elements(self) -> None:
        position = Position.objects.create(
            name="director"
        )
        username = "test_user"
        password = "user12345"
        employee = get_user_model().objects.create_user(
            username=username,
            password=password,
            position=position
        )
        team = Team.objects.create(
            name="Developers"
        )
        pr_type = ProjectType.objects.create(
            name="DEV"
        )
        pr_name = "Develop model Atlant"
        project = Project.objects.create(
            name=pr_name,
            is_completed=False,
            owner=employee,
            team=team,
            project_type=pr_type
        )
        task_name = "Design the sofa seat"
        task = Task.objects.create(
            name=task_name,
            is_completed=False,
            project=project
        )

        self.assertEqual(task.project.name, pr_name)
        self.assertEqual(task.is_completed, False)
        self.assertEqual(task.priority, "B")
        self.assertEqual(task.project.team, team)
        self.assertEqual(task.project.project_type, pr_type)
        self.assertEqual(task.name, task_name)
        self.assertEqual(task.project, project)
