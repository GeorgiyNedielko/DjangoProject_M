from rest_framework import serializers
from .models import Task


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task

        fields = (
            "id",
            "title",
            "description",
            "status",
            "due_date",
            "project",
            "priority",
        )

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = "__all__"