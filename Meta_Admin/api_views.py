from django.utils import timezone
from django.db.models import Count
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Task, SubTask
from .serializers import (
    TaskCreateSerializer,
    TaskSerializer,
    SubTaskSerializer,
    SubTaskCreateSerializer,
)


# ===== Функции для Task (они у тебя уже были) =====

@api_view(["POST"])
def create_task(request):
    serializer = TaskCreateSerializer(data=request.data)
    if serializer.is_valid():
        task = serializer.save()
        return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def tasks_list(request):
    """
    Получение списка задач.
    """
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def task_detail(request, pk):
    """
    Получение одной задачи по её ID.
    """
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response({"detail": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = TaskSerializer(task)
    return Response(serializer.data)


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


# ===== Классы для SubTask (задание 13) =====

class SubTaskListCreateView(APIView):
    """
    GET  /api/subtasks/       -> список всех подзадач
    POST /api/subtasks/       -> создание подзадачи
    """

    def get(self, request):
        subtasks = SubTask.objects.all()
        serializer = SubTaskSerializer(subtasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SubTaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            subtask = serializer.save()
            out_serializer = SubTaskSerializer(subtask)
            return Response(out_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubTaskDetailUpdateDeleteView(APIView):
    """
    GET    /api/subtasks/<id>/   -> получить подзадачу
    PUT    /api/subtasks/<id>/   -> полное обновление
    PATCH  /api/subtasks/<id>/   -> частичное обновление
    DELETE /api/subtasks/<id>/   -> удалить подзадачу
    """

    def get_object(self, pk):
        return get_object_or_404(SubTask, pk=pk)

    def get(self, request, pk):
        subtask = self.get_object(pk)
        serializer = SubTaskSerializer(subtask)
        return Response(serializer.data)

    def put(self, request, pk):
        subtask = self.get_object(pk)
        serializer = SubTaskCreateSerializer(subtask, data=request.data)
        if serializer.is_valid():
            subtask = serializer.save()
            out_serializer = SubTaskSerializer(subtask)
            return Response(out_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        subtask = self.get_object(pk)
        serializer = SubTaskCreateSerializer(subtask, data=request.data, partial=True)
        if serializer.is_valid():
            subtask = serializer.save()
            out_serializer = SubTaskSerializer(subtask)
            return Response(out_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        subtask = self.get_object(pk)
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
