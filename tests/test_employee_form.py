from django.test import TestCase

from task_manager.forms import EmployeeCreationForm, EmployeeSearchForm


class EmployeeFormTests(TestCase):
    def employee_creation_form_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user12345",
            "password2": "user12345",
            "first_name": "first_name",
            "last_name": "last_name",
            "position": "Director"
        }
        form = EmployeeCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class EmployeeSearchFormTestCase(TestCase):
    def test_valid_form(self):
        form_data = {
            'username': 'JohnDoe',
        }
        form = EmployeeSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            'username': '',
        }
        form = EmployeeSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
