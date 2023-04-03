from django import forms

from task_manager.models import Commentary


class CommentaryCreateForm(forms.ModelForm):
    class Meta:
        model = Commentary
        fields = ["content"]
