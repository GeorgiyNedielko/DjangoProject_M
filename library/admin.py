from django.contrib import admin
from .models import (Author, Book, Library, Member, Category, Posts, Borrow,
                     Review, AuthorDetail, Event, EventParticipant, Task, SubTask)


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

# ДЗ_8 (https://lms.itcareerhub.de/mod/assign/view.php?id=7551), админка из моделей


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'deadline', 'created_at', 'categories')
    search_fields = ('title', 'description')
    filter_horizontal = ('categories',)
    ordering = ('-created_at',)


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'deadline', 'created_at', 'task')
    search_fields = ('title', 'description', 'task__title')
    ordering = ('-created_at',)
