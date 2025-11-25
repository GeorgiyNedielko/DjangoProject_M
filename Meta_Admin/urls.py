from django.urls import path
from . import api_views

urlpatterns = [
    # Задание 1
    path("api/tasks/create/", api_views.create_task, name="task-create"),

    # Задание 2
    path("api/tasks/", api_views.tasks_list, name="tasks-list"),
    path("api/tasks/<int:pk>/", api_views.task_detail, name="task-detail"),

    # Задание 3
    path("api/tasks/stats/", api_views.tasks_stats, name="tasks-stats"),
]
