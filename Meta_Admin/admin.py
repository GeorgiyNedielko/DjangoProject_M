from django.contrib import admin
from django import forms
from django.shortcuts import render, redirect

from .models import Project, Task, Tag, ProjectFile, SubTask, Category


class ReplaceCharactersForm(forms.Form):
    old_char = forms.CharField(label="Старый символ", max_length=10)
    new_char = forms.CharField(label="Новый символ", max_length=10)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "count_of_files", "created_at")
    actions = ["replace_characters"]

    @admin.action(description="Заменить символы в названии")
    def replace_characters(self, request, queryset):
        # Нажали кнопку "Выполнить замену" на нашей форме
        if "apply" in request.POST:
            form = ReplaceCharactersForm(request.POST)
            if form.is_valid():
                old_char = form.cleaned_data["old_char"]
                new_char = form.cleaned_data["new_char"]

                for obj in queryset:
                    if obj.name:
                        obj.name = obj.name.replace(old_char, new_char)
                        obj.save()

                self.message_user(request, "Символы в названиях успешно заменены")
                return redirect(request.get_full_path())
        else:
            # Первый заход — просто показываем форму
            form = ReplaceCharactersForm()

        context = {
            "form": form,
            "queryset": queryset,
        }
        return render(request, "admin/replace_characters.html", context)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "project", "status", "priority", "assignee", "due_date")
    list_filter = ("status", "priority", "project")
    search_fields = ("title", "description")

    actions = [
        "set_status_closed",
        "set_status_new",
        "set_priority_low",
        "set_priority_medium",
        "set_priority_high",
        "set_priority_very_high",
    ]

    # ---------- СТАТУСЫ ----------

    @admin.action(description="Статус: Закрыто")
    def set_status_closed(self, request, queryset):
        updated = queryset.update(status="Closed")
        self.message_user(request, f"Статус 'Closed' установлен у {updated} задач.")

    @admin.action(description="Статус: Новая")
    def set_status_new(self, request, queryset):
        updated = queryset.update(status="New")
        self.message_user(request, f"Статус 'New' установлен у {updated} задач.")

    # ---------- ПРИОРИТЕТЫ ----------

    @admin.action(description="Приоритет: Низкий")
    def set_priority_low(self, request, queryset):
        updated = queryset.update(priority="Low")
        self.message_user(request, f"Приоритет 'Low' установлен у {updated} задач.")

    @admin.action(description="Приоритет: Средний")
    def set_priority_medium(self, request, queryset):
        updated = queryset.update(priority="Medium")
        self.message_user(request, f"Приоритет 'Medium' установлен у {updated} задач.")

    @admin.action(description="Приоритет: Высокий")
    def set_priority_high(self, request, queryset):
        updated = queryset.update(priority="High")
        self.message_user(request, f"Приоритет 'High' установлен у {updated} задач.")

    @admin.action(description="Приоритет: Очень высокий")
    def set_priority_very_high(self, request, queryset):
        updated = queryset.update(priority="Very High")
        self.message_user(request, f"Приоритет 'Very High' установлен у {updated} задач.")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)


@admin.register(ProjectFile)
class ProjectFileAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")

from .models import Project, Task, Tag, ProjectFile, SubTask, Category


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "task", "status", "created_at")
    list_filter = ("task", "status")
    search_fields = ("title", "description", "task__title")
    ordering = ("-created_at",)

    actions = [
        "set_status_new",
        "set_status_pending",
        "set_status_in_progress",
        "set_status_closed",
    ]

    @admin.action(description="Статус подзадачи: New")
    def set_status_new(self, request, queryset):
        updated = queryset.update(status=Task.STATUS_NEW)
        self.message_user(request, f"Статус 'New' установлен у {updated} подзадач.")

    @admin.action(description="Статус подзадачи: Pending")
    def set_status_pending(self, request, queryset):
        updated = queryset.update(status=Task.STATUS_PENDING)
        self.message_user(request, f"Статус 'Pending' установлен у {updated} подзадач.")

    @admin.action(description="Статус подзадачи: In Progress")
    def set_status_in_progress(self, request, queryset):
        updated = queryset.update(status=Task.STATUS_IN_PROGRESS)
        self.message_user(request, f"Статус 'In Progress' установлен у {updated} подзадач.")

    @admin.action(description="Статус подзадачи: Closed")
    def set_status_closed(self, request, queryset):
        updated = queryset.update(status=Task.STATUS_CLOSED)
        self.message_user(request, f"Статус 'Closed' установлен у {updated} подзадач.")



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)

