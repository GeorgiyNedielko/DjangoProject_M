from django.utils import timezone

from .models import Task, SubTask, Category

from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = ("username", "email", "password", "password2")
        extra_kwargs = {
            "email": {"required": True},
        }

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует.")
        return value

    def validate(self, attrs):

        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Пароли не совпадают."})


        try:
            validate_password(attrs["password"])
        except Exception as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        password = validated_data.pop("password")

        user = User(
            username=validated_data["username"],
            email=validated_data["email"],
        )
        user.set_password(password)
        user.save()
        return user

class TaskSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения задач (list, detail)."""
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Task
        fields = "__all__"


class TaskCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания/обновления задач с валидацией due_date."""
    class Meta:
        model = Task

        exclude = ("owner",)

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




class SubTaskSerializer(serializers.ModelSerializer):
    """Обычный сериализатор для отображения подзадач."""
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = SubTask
        fields = "__all__"


class SubTaskCreateSerializer(serializers.ModelSerializer):
    """Создание/обновление SubTask. created_at и owner только для чтения."""
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SubTask
        exclude = ("owner",)




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
