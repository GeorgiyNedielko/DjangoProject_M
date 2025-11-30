from rest_framework import serializers
from django.utils import timezone

from .models import Task, SubTask, Category


# ===== Task serializers =====

class TaskSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения задач (list, detail)."""
    class Meta:
        model = Task
        fields = "__all__"


class TaskCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания/обновления задач с валидацией due_date."""

    class Meta:
        model = Task
        fields = "__all__"

    def validate_due_date(self, value):
        """
        Нельзя ставить срок выполнения задачи в прошлом.
        """
        if value is None:
            return value  # поле необязательное

        now = timezone.now()
        if value < now:
            raise serializers.ValidationError(
                "Дата и время дедлайна (due_date) не могут быть в прошлом."
            )
        return value


# ===== SubTask serializers =====

class SubTaskSerializer(serializers.ModelSerializer):
    """Обычный сериализатор для отображения подзадач."""
    class Meta:
        model = SubTask
        fields = "__all__"


class SubTaskCreateSerializer(serializers.ModelSerializer):
    """Создание/обновление SubTask. created_at только для чтения."""
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SubTask
        fields = "__all__"


# ===== Category serializers =====

class CategoryCreateSerializer(serializers.ModelSerializer):
    """Создание/обновление Category с проверкой уникальности name."""
    class Meta:
        model = Category
        fields = "__all__"

    def validate_name(self, value):
        qs = Category.objects.filter(name__iexact=value)
        if self.instance is not None:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError(
                "Категория с таким названием уже существует."
            )
        return value

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


# ===== TaskDetailSerializer с вложенными подзадачами =====

class TaskDetailSerializer(serializers.ModelSerializer):
    """
    Детальный сериализатор задачи с вложенными SubTask.
    Использует related_name='subtasks' из модели SubTask.
    """
    subtasks = SubTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "priority",
            "project",
            "assignee",
            "created_at",
            "updated_at",
            "deleted_at",
            "due_date",
            "tags",
            "subtasks",
        ]
