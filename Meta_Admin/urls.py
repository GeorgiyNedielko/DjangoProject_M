from django.urls import path
from . import api_views
from .api_views import (
    TaskListCreateView,
    TaskDetailView,
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView,
    subtask_statuses,
    subtasks_by_weekday,
)

urlpatterns = [

    # TASKS — GENERIC VIEWS
    path("api/tasks/", TaskListCreateView.as_view(), name="tasks-list-create"),
    path("api/tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("api/tasks/stats/", api_views.tasks_stats, name="tasks-stats"),

    # Задание 13 — SubTask
    path("api/subtasks/", SubTaskListCreateView.as_view(), name="subtask-list-create"),
    path("api/subtasks/<int:pk>/", SubTaskDetailUpdateDeleteView.as_view(), name="subtask-detail"),

    # СТАТУСЫ ПОДЗАДАЧ
    path("subtasks/statuses/", subtask_statuses, name="subtask-statuses"),

    # weekda
    path("api/subtasks/day/<str:weekday>/", api_views.subtasks_by_weekday),
]


