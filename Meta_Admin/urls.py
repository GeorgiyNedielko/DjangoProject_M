from django.urls import path
from . import api_views
from .api_views import SubTaskListCreateView, SubTaskDetailUpdateDeleteView

urlpatterns = [
    # Задание 11, 12 (твои задачи)
    path("api/tasks/create/", api_views.create_task, name="task-create"),
    path("api/tasks/", api_views.tasks_list, name="tasks-list"),
    path("api/tasks/<int:pk>/", api_views.task_detail, name="task-detail"),
    path("api/tasks/stats/", api_views.tasks_stats, name="tasks-stats"),

    # Задание 13 — SubTask
    path("subtasks/", SubTaskListCreateView.as_view(), name="subtask-list-create"),
    path("subtasks/<int:pk>/", SubTaskDetailUpdateDeleteView.as_view(), name="subtask-detail"),
]
