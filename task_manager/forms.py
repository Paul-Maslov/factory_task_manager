from django import forms

from task_manager.models import Commentary, Task


class CommentaryCreateForm(forms.ModelForm):
    class Meta:
        model = Commentary
        fields = ["content"]


class TasksCreateForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ["description"]
