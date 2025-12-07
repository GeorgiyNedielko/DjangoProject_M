from django.utils import timezone
from django.db.models import Count

from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from django_filters.rest_framework import DjangoFilterBackend

from .models import Task, SubTask
from .serializers import (
    TaskCreateSerializer,
    TaskSerializer,
    SubTaskSerializer,
    SubTaskCreateSerializer,
)


class ProtectedDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "message": "Hello, authenticated user!",
            "user": request.user.username
        })


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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return TaskCreateSerializer
        return TaskSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
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
@permission_classes([AllowAny])
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
    permission_classes = [IsAuthenticated]
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


class SubTaskDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/subtasks/<id>/
    PUT    /api/subtasks/<id>/
    PATCH  /api/subtasks/<id>/
    DELETE /api/subtasks/<id>/
    """
    queryset = SubTask.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return SubTaskCreateSerializer
        return SubTaskSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
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
    page = paginator.paginate_queryset(queryset, request)

    serializer = SubTaskSerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)
