from django.urls import path, include

from task_manager.views import index, about


urlpatterns = [
    path("", index, name="index"),
    path("about/", about, name="about"),


]

app_name = "task_manager"
