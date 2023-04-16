from django.test import TestCase, Client

from django.urls import reverse

INDEX_URL = reverse("task_manager:index")
ABOUT_URL = reverse("task_manager:about")


class PublicMainTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_index_login_not_required(self):
        res = self.client.get(INDEX_URL)

        self.assertEqual(res.status_code, 200)

    def test_about_login_not_required(self):
        res = self.client.get(ABOUT_URL)

        self.assertEqual(res.status_code, 200)
