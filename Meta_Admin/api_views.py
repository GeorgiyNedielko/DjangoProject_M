from django.utils import timezone
from django.db.models import Count
from django.shortcuts import get_object_or_404

from rest_framework import generics, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from .models import Task, SubTask
from .serializers import (
    TaskCreateSerializer,
    TaskSerializer,
    SubTaskSerializer,
    SubTaskCreateSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend

DAY_NAME_TO_WEEKDAY = {
    "sunday": 1,
    "воскресенье": 1,

    "monday": 2,
    "понедельник": 2,

    "tuesday": 3,
    "вторник": 3,

    "wednesday": 4,
    "среда": 4,

    "thursday": 5,
    "четверг": 5,

    "friday": 6,
    "пятница": 6,

    "saturday": 7,
    "суббота": 7,
}


# ---------- TASKS ----------

class TaskListCreateView(generics.ListCreateAPIView):
    """
    GET /api/tasks/   -> список задач (с фильтрами, поиском, сортировкой)
    POST /api/tasks/  -> создание задачи
    """
    queryset = Task.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    # фильтрация по статусу и дедлайну
    filterset_fields = ["status", "due_date"]

    # поиск по названию и описанию
    search_fields = ["title", "description"]

    # сортировка по дате создания
    ordering_fields = ["created_at"]
    ordering = ["created_at"]  # сортировка по умолчанию

    def get_serializer_class(self):
        if self.request.method == "POST":
            return TaskCreateSerializer
        return TaskSerializer

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/tasks/<id>/ -> получить задачу
    PUT    /api/tasks/<id>/ -> полное обновление
    PATCH  /api/tasks/<id>/ -> частичное обновление
    DELETE /api/tasks/<id>/ -> удалить
    """
    queryset = Task.objects.all()

    def get_serializer_class(self):

        if self.request.method in ["PUT", "PATCH"]:
            return TaskCreateSerializer
        return TaskSerializer


# @api_view(["POST"])
# def create_task(request):
#     serializer = TaskCreateSerializer(data=request.data)
#     if serializer.is_valid():
#         task = serializer.save()
#         return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(["GET"])
# def tasks_list(request):
#     """
#     Получение списка задач.
#
#     Если параметр ?day_of_week не передан — вернуть все задачи.
#     Если передан — отфильтровать задачи по дню недели поля due_date.
#     Пример: /api/tasks/?day_of_week=вторник
#     """
#     tasks = Task.objects.all()
#
#     day_param = request.query_params.get("day_of_week")
#
#     # Параметр не передан — возвращаем все задачи
#     if not day_param:
#         serializer = TaskSerializer(tasks, many=True)
#         return Response(serializer.data)
#
#     # Параметр передан — фильтруем по дню недели
#     day_name = day_param.strip().lower()
#     weekday_num = DAY_NAME_TO_WEEKDAY.get(day_name)
#
#     if weekday_num is None:
#         return Response(
#             {
#                 "detail": "Некорректный день недели.",
#                 "allowed_values": list(DAY_NAME_TO_WEEKDAY.keys()),
#             },
#             status=status.HTTP_400_BAD_REQUEST,
#         )
#
#     # Фильтрация по полю due_date
#     tasks = tasks.filter(due_date__week_day=weekday_num)
#
#     serializer = TaskSerializer(tasks, many=True)
#     return Response(serializer.data)
#
#
# @api_view(["GET"])
# def task_detail(request, pk):
#     """
#     Получение одной задачи по её ID.
#     """
#     try:
#         task = Task.objects.get(pk=pk)
#     except Task.DoesNotExist:
#         return Response({"detail": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
#
#     serializer = TaskSerializer(task)
#     return Response(serializer.data)


@api_view(["GET"])
def tasks_stats(request):
    """
    Статистика задач:
    - общее количество
    - количество по каждому статусу
    - количество просроченных задач (due_date < сейчас)
    """

    now = timezone.now()
    qs = Task.objects.filter(deleted_at__isnull=True)

    total_tasks = qs.count()
    tasks_by_status = qs.values("status").annotate(count=Count("id"))
    overdue_tasks = qs.filter(due_date__lt=now).count()

    data = {
        "total_tasks": total_tasks,
        "tasks_by_status": list(tasks_by_status),
        "overdue_tasks": overdue_tasks,
    }
    return Response(data)

@api_view(["GET"])
def subtask_statuses(request):
    """
    GET /api/subtasks/statuses/
    Возвращает список доступных статусов подзадач
    """
    statuses = [choice[0] for choice in SubTask.STATUS_CHOICES]
    return Response({"available_statuses": statuses})

# ---------- SUBTASKS ----------

class SubTaskPagination(PageNumberPagination):
    """
    Пагинация для подзадач:
    по 5 объектов на страницу, без возможности менять размер страницы.
    """
    page_size = 5
    page_size_query_param = None
    max_page_size = 5

class SubTaskListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/subtasks/   -> список подзадач (с пагинацией, фильтрацией, поиском, сортировкой)
    POST /api/subtasks/   -> создание подзадачи
    """
    queryset = SubTask.objects.all()
    pagination_class = SubTaskPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # фильтрация по статусу и дедлайну
    filterset_fields = ["status", "deadline"]

    # поиск по названию и описанию
    search_fields = ["title", "description"]

    # сортировка по дате создания
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return SubTaskCreateSerializer
        return SubTaskSerializer

# class SubTaskListCreateView(APIView):
#     """
#     GET  /api/subtasks/       -> список всех подзадач (с пагинацией, сортировка по -created_at)
#     POST /api/subtasks/       -> создание подзадачи
#     """
#
#     def get(self, request):
#         """
#         Фильтры:
#         - ?task_title=...  -> по названию главной задачи (Task.title, icontains)
#         - ?status=...      -> по статусу подзадачи (status, iexact)
#
#         Если фильтры не переданы — вернётся обычный список с пагинацией.
#         """
#
#         # Базовый queryset: все подзадачи, самые новые сначала
#         queryset = SubTask.objects.order_by("-created_at")
#
#         # --- читаем фильтры из query-параметров ---
#         task_title = request.query_params.get("task_title")
#         status_param = request.query_params.get("status")
#
#         # Фильтр по названию главной задачи
#         if task_title:
#             queryset = queryset.filter(task__title__icontains=task_title)
#
#         # Фильтр по статусу подзадачи
#         if status_param:
#             queryset = queryset.filter(status__iexact=status_param)
#
#         # --- пагинация ---
#         paginator = SubTaskPagination()
#         page = paginator.paginate_queryset(queryset, request)
#
#         serializer = SubTaskSerializer(page, many=True)
#         return paginator.get_paginated_response(serializer.data)
#
#     def post(self, request):
#         serializer = SubTaskCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             subtask = serializer.save()
#             out_serializer = SubTaskSerializer(subtask)
#             return Response(out_serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubTaskDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/subtasks/<id>/
    PUT    /api/subtasks/<id>/
    PATCH  /api/subtasks/<id>/
    DELETE /api/subtasks/<id>/
    """
    queryset = SubTask.objects.all()

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return SubTaskCreateSerializer
        return SubTaskSerializer


# class SubTaskDetailUpdateDeleteView(APIView):
#     """
#     GET    /api/subtasks/<id>/   -> получить подзадачу
#     PUT    /api/subtasks/<id>/   -> полное обновление
#     PATCH  /api/subtasks/<id>/   -> частичное обновление
#     DELETE /api/subtasks/<id>/   -> удалить подзадачу
#     """
#
#     def get_object(self, pk):
#         return get_object_or_404(SubTask, pk=pk)
#
#     def get(self, request, pk):
#         subtask = self.get_object(pk)
#         serializer = SubTaskSerializer(subtask)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         subtask = self.get_object(pk)
#         serializer = SubTaskCreateSerializer(subtask, data=request.data)
#         if serializer.is_valid():
#             subtask = serializer.save()
#             out_serializer = SubTaskSerializer(subtask)
#             return Response(out_serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def patch(self, request, pk):
#         subtask = self.get_object(pk)
#         serializer = SubTaskCreateSerializer(subtask, data=request.data, partial=True)
#         if serializer.is_valid():
#             subtask = serializer.save()
#             out_serializer = SubTaskSerializer(subtask)
#             return Response(out_serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         subtask = self.get_object(pk)
#         subtask.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["GET"])
def subtasks_by_weekday(request, weekday):
    """
    GET /api/subtasks/day/sunday
    Фильтрация подзадач по дню недели главной задачи.
    """
    weekday = weekday.lower()
    weekday_num = DAY_NAME_TO_WEEKDAY.get(weekday)

    if not weekday_num:
        return Response(
            {
                "detail": "Некорректный день недели.",
                "allowed_values": list(DAY_NAME_TO_WEEKDAY.keys())
            },
            status=400
        )

    queryset = SubTask.objects.filter(task__due_date__week_day=weekday_num).order_by("-created_at")

    paginator = SubTaskPagination()
    page = paginator.paginate_queryset(queryset,request)

    serializer = SubTaskSerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)


