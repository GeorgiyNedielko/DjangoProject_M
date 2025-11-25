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
        validators=[MinLengthValidator(10)],
        unique=True,
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

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_task'
        ordering = ['-created_at']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

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

class SubTask(models.Model):
    title = models.CharField(max_length=255,
                             unique=True,)
    description = models.TextField(null=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks', verbose_name='Задача',)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True, blank=True, verbose_name="Дедлайн")

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_subtask'
        ordering = ['-created_at']
        verbose_name = 'SubTask'
        verbose_name_plural = 'SubTasks'

class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
