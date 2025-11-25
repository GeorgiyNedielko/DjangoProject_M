from django.contrib import admin
from django.utils import timezone
from .models import (
    Author,
    Book,
    Library,
    Member,
    Category,
    Posts,
    Borrow,
    Review,
    AuthorDetail,
    Event,
    EventParticipant,
    Task,
    SubTask,
    Publisher,
)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'role', 'active')
    list_filter = ('role', 'active', 'libraries')
    search_fields = ('first_name', 'last_name', 'email')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'publisher', 'library', 'published_date', 'genre')
    list_filter = ('genre', 'library', 'author', 'publisher')
    search_fields = ('name', 'author__first_name', 'author__last_name')

    def update_created_at(self, request, queryset):
        queryset.update(created_at=timezone.now())

    update_created_at.short_description = "Обновить created_at на текущее время"
    actions = ["update_created_at"]   # actions — строкой, всё ок

# ВАЖНО: вот эту строку УДАЛЯЕМ, она лишняя и ломает:
# admin.site.register(Book, BookAdmin)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'rating', 'is_deleted')
    list_filter = ('is_deleted', 'rating')
    search_fields = ('first_name', 'last_name')


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'library', 'created_at', 'is_moderated')
    list_filter = ('library', 'author', 'is_moderated', 'created_at')
    search_fields = ('title', 'text', 'author__first_name', 'author__last_name')
    ordering = ('-created_at',)


@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = (
        'member',
        'book',
        'library',
        'borrow_date',
        'return_date',
        'is_returned',
        'overdue_status',
    )
    list_filter = (
        'library',
        'is_returned',
        'borrow_date',
        'return_date',
    )
    search_fields = (
        'member__first_name',
        'member__last_name',
        'book__name',
    )
    ordering = ('-borrow_date',)

    def overdue_status(self, obj):
        """Показывает: просрочена книга или нет."""
        return "Да" if obj.is_overdue() else "Нет"

    overdue_status.short_description = "Просрочено?"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'reviewer', 'rating', 'created_at')
    list_filter = ('rating', 'created_at', 'book')
    search_fields = ('book__name', 'reviewer__first_name', 'reviewer__last_name', 'text')


@admin.register(AuthorDetail)
class AuthorDetailAdmin(admin.ModelAdmin):
    list_display = ('author', 'gender', 'birth_city')
    search_fields = ('author__first_name', 'author__last_name', 'birth_city')
    list_filter = ('gender',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'library')
    list_filter = ('library', 'event_date')
    search_fields = ('title', 'description')
    filter_horizontal = ('books',)


@admin.register(EventParticipant)
class EventParticipantAdmin(admin.ModelAdmin):
    list_display = ('event', 'member', 'registration_date')
    list_filter = ('event', 'registration_date', 'member')
    search_fields = ('event__title', 'member__first_name', 'member__last_name')


# ======== Инлайн для SubTask и админка Task (Задание 1+2) ========

class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_title', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'deadline', 'created_at', 'categories')
    search_fields = ('title', 'description')
    filter_horizontal = ('categories',)
    ordering = ('-created_at',)
    inlines = [SubTaskInline]

    def short_title(self, obj):
        title = obj.title or ""
        return title[:10] + "..." if len(title) > 10 else title

    short_title.short_description = "Название"


# ======== SubTask + action "в Done" (Задание 3) ========

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'deadline', 'created_at', 'task')
    search_fields = ('title', 'description', 'task__title')
    ordering = ('-created_at',)
    actions = ["mark_as_done"]

    def mark_as_done(self, request, queryset):
        updated = queryset.update(status="done")  # проверь, что в модели статус именно "done"
        self.message_user(request, f"Переведено в Done: {updated} подзадач.")

    mark_as_done.short_description = "Перевести выбранные подзадачи в статус Done"


# ======== Inline для книг издателя ========

class BookInline(admin.TabularInline):
    model = Book
    extra = 1


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "established_date")
    search_fields = ("name",)
    list_filter = ("established_date",)
    ordering = ("name",)
    inlines = [BookInline]
