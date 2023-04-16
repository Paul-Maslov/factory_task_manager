from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.models import Team, ProjectType, Project, Task, Post


class PostFormTests(TestCase):
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
        pr_name = "Develop model Atlant"
        self.project = Project.objects.create(
            name=pr_name,
            is_completed=False,
            owner=self.employee,
            team=self.team,
            project_type=self.project_type
        )
        task_name = "Design the sofa seat"
        self.task = Task.objects.create(
            name=task_name,
            is_completed=False,
            project=self.project
        )

    def test_create_post(self):
        post_name = "Test creation post"
        response = self.client.post(
            reverse(
                "task_manager:post-create"
            ),
            {
                "title": post_name,
                "content": "Try to create new post",
                "owner": self.user.id,
                "task": self.task.id
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.get(id=1).title, "Test creation post")
        self.assertEqual(Post.objects.get(id=1).content, "Try to create new post")

    def test_update_post(self):
        post_name = "Test creation post"
        post = Post.objects.create(
            title=post_name,
            content="Try to create new post",
            owner=self.employee,
            task=self.task
        )
        response = self.client.post(
            reverse(
                "task_manager:post-update",
                kwargs={"pk": post.id}
            ),
            {
                "pk": post.id,
                "title": "Test updating post",
                "content": "Try to update new post",
                "owner": self.employee.id,
                "task": self.task.id

            },
        )
        Post.objects.get(id=post.id).refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.get(id=post.id).title, "Test updating post")
        self.assertEqual(Post.objects.get(id=post.id).content, "Try to update new post")

    def test_delete_post(self):
        post_name = "Test deletion post"
        post = Post.objects.create(
            title=post_name,
            content="Try to delete post",
            owner=self.employee,
            task=self.task
        )
        response = self.client.post(
            reverse(
                "task_manager:post-delete",
                kwargs={"pk": post.id}
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(id=post.id).exists())
