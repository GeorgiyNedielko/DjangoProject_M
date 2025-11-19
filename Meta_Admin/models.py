from django.db import models

from django.db import models
from django.core.validators import MinLengthValidator, MaxValueValidator
from django.contrib.auth.models import User
from django import forms
from django.shortcuts import render, redirect

class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    files = models.ManyToManyField(
        'ProjectFile',
        blank=True,
        related_name='projects',
        verbose_name='Файлы'
    )

    class Meta:
        ordering = ['-name']
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'description'],
                name='unique_project_name_description'
            )
        ]

    def __str__(self):
        return self.name

    @property
    def count_of_files(self):
        """Кол-во файлов, связанных с этим проектом."""
        return self.files.count()



STATUSES_CHOICES = [
    ('New', 'New'),
    ('In_progress', 'In_progress'),
    ('Completed', 'Completed'),
    ('Closed', 'Closed'),
    ('Pending', 'Pending'),
    ('Blocked', 'Blocked'),
]

PRIORITY_CHOICES = [
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High'),
    ('Very High', 'Very High'),
]


class Task(models.Model):
    title = models.CharField(
        max_length=255,
        validators=[MinLengthValidator(10)]
    )
    description = models.TextField(null=True, blank=True)

    status = models.CharField(max_length=15, choices=STATUSES_CHOICES, default='New')
    priority = models.CharField(max_length=15, choices=PRIORITY_CHOICES)

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks_assigned',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    due_date = models.DateTimeField(null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='tasks')

    class Meta:
        # 1. Названия модели
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

        # 2. Порядок отображения:
        #    сначала по дате сдачи (от самой дальней к ближайшей),
        #    потом по закреплённому сотруднику
        ordering = ['-due_date', 'assignee']

        # 3. Уникальность по названию + проекту
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'project'],
                name='unique_task_title_project',
            )
        ]

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-due_date', '-priority']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        unique_together = (('title', 'project'),)

class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class ProjectFile(models.Model):
    name = models.CharField(
        max_length=120,
        verbose_name='Название файла'
    )
    file = models.FileField(
        upload_to='projects/',           # файлы будут попадать в папку "projects"
        verbose_name='Файл'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания файла'
    )

    class Meta:
        verbose_name = 'Файл проекта'
        verbose_name_plural = 'Файлы проекта'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

