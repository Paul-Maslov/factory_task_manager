from django import forms
from django.contrib.auth.forms import UserCreationForm

from task_manager.models import Employee
from task_manager.models import Commentary, Task


class EmployeeCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Employee
        fields = UserCreationForm.Meta.fields + \
            ("first_name", "last_name",  "position", "photo")


class CommentaryCreateForm(forms.ModelForm):
    class Meta:
        model = Commentary
        fields = ["content"]


class EmployeeSearchForm(forms.Form):
    username = forms.CharField(
        max_length=70,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by employee:"})
    )


class ProjectSearchForm(forms.Form):
    name = forms.CharField(
        max_length=70,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by project title:"}
        )
    )


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("fact_date",)
        widgets = {
            "fact_date": forms.DateInput(attrs={"type": "date"})
        }


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=70,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by task title:"})
    )


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("fact_date",)
        widgets = {
            "fact_date": forms.DateInput(attrs={"type": "date"})
        }


class PostSearchForm(forms.Form):
    title = forms.CharField(
        max_length=70,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by post:"})
    )


class TasksCreateForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ["description"]
