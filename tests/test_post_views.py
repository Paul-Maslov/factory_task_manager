from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from django.urls import reverse

from task_manager.models import (
    Post, Position, Team,
    ProjectType, Project, Task,
    Commentary,
)

POST_URL = reverse("task_manager:post-list")


class PublicPostTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_list_login_required(self):
        res = self.client.get(POST_URL)

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
        task_name = "Design the sofa seat"
        self.task = Task.objects.create(
            name=task_name,
            is_completed=False,
            project=self.project
        )

    def test_post_list_response_with_correct_template(self):
        response = self.client.get(POST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "task_manager/post_list.html")

    def test_retrieve_posts_with_all_components(self):
        self.post1 = Post.objects.create(
            title="Test post first",
            content="Content of first test post",
            owner=self.employee,
            task=self.task
        )
        self.post2 = Post.objects.create(
            title="Test post second",
            content="Content of second post",
            owner=self.employee,
            task=self.task
        )
        response = self.client.get(POST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post2.title)
        self.assertTemplateUsed(response, "task_manager/post_list.html")
        self.assertContains(response, self.post1.task.name[1])
        self.assertContains(response, self.post2.task.project.name[1])

    def test_search_post_form(self):
        response = self.client.get(POST_URL + "?name=develop")

        self.assertContains(response, "develop")
        self.assertNotContains(response, "modernization")
        self.assertTemplateUsed(response, "task_manager/post_list.html")

    def test_post_detail_with_new_commentary(self):
        self.post1 = Post.objects.create(
            title="Test post first",
            content="Content of first test post",
            owner=self.employee,
            task=self.task
        )
        Commentary.objects.create(
            content="Something commentary",
            user=self.employee,
            post_id=1
        )

        response = self.client.get(reverse("task_manager:post-detail", args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "task_manager/post_detail.html")


