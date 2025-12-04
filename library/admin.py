from django.contrib import admin
from django.utils import timezone

from .models import (
    Author,
    Book,
    DeletedBook,
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
    Supplier,
    Genre,
)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "role", "active")
    list_filter = ("role", "active", "libraries")
    search_fields = ("first_name", "last_name", "email")


# ==== КНИГИ ====


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Активные (не удалённые) книги.
    """

    list_display = (
        "name",
        "author",
        "publisher",
        "library",
        "category",
        "genre",
        "price",
        "discounted_price",
        "is_bestseller",
        "rating",
        "published_date",
    )
    list_filter = (
        "genre",
        "category",
        "library",
        "author",
        "publisher",
        "is_bestseller",
    )
    search_fields = ("name", "author__first_name", "author__last_name")
    readonly_fields = ("rating",)
    actions = ["update_created_at"]

    fieldsets = (
        ("Основная информация", {
            "fields": ("name", "author", "library", "publisher", "category", "genre")
        }),
        ("Описание и параметры", {
            "fields": ("description", "pages"),
        }),
        ("Цена и статус", {
            "fields": ("price", "discounted_price", "is_bestseller"),
        }),
        ("Служебные данные", {
            "fields": ("published_date", "created_at", "rating"),
            "classes": ("collapse",),
        }),
    )

    def get_queryset(self, request):
        # На всякий случай — показываем только не удалённые
        qs = super().get_queryset(request)
        return qs.filter(is_deleted=False)

    def update_created_at(self, request, queryset):
        queryset.update(created_at=timezone.now())

    update_created_at.short_description = "Обновить created_at на текущее время"


@admin.register(DeletedBook)
class DeletedBookAdmin(admin.ModelAdmin):
    """
    Отдельный раздел для удалённых книг (is_deleted=True).
    """

    list_display = (
        "name",
        "author",
        "publisher",
        "library",
        "category",
        "genre",
        "price",
        "discounted_price",
        "is_bestseller",
        "published_date",
    )
    list_filter = (
        "genre",
        "category",
        "library",
        "author",
        "publisher",
        "is_bestseller",
    )
    search_fields = ("name", "author__first_name", "author__last_name")
    actions = ["restore_books"]

    fieldsets = (
        ("Основная информация", {
            "fields": ("name", "author", "library", "publisher", "category", "genre")
        }),
        ("Описание и параметры", {
            "fields": ("description", "pages"),
        }),
        ("Цена и статус", {
            "fields": ("price", "discounted_price", "is_bestseller"),
        }),
        ("Служебные данные", {
            "fields": ("published_date", "created_at"),
            "classes": ("collapse",),
        }),
    )

    def get_queryset(self, request):
        # Показываем только удалённые книги
        return self.model.all_objects.filter(is_deleted=True)

    def restore_books(self, request, queryset):
        """
        Action: восстановить выбранные книги.
        """
        updated = queryset.update(is_deleted=False)
        self.message_user(request, f"Восстановлено книг: {updated}")

    restore_books.short_description = "Восстановить выбранные книги"


# ===== Author + AuthorDetail inline =====


class AuthorDetailInline(admin.StackedInline):
    model = AuthorDetail
    extra = 0
    max_num = 1


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "rating", "is_deleted")
    list_filter = ("is_deleted", "rating")
    search_fields = ("first_name", "last_name")
    inlines = [AuthorDetailInline]


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "library", "created_at", "is_moderated")
    list_filter = ("library", "author", "is_moderated", "created_at")
    search_fields = ("title", "text", "author__first_name", "author__last_name")
    ordering = ("-created_at",)


@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = (
        "member",
        "book",
        "library",
        "borrow_date",
        "return_date",
        "is_returned",
        "overdue_status",
    )
    list_filter = (
        "library",
        "is_returned",
        "borrow_date",
        "return_date",
    )
    search_fields = (
        "member__first_name",
        "member__last_name",
        "book__name",
    )
    ordering = ("-borrow_date",)

    def overdue_status(self, obj):
        return "Да" if obj.is_overdue() else "Нет"

    overdue_status.short_description = "Просрочено?"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("book", "reviewer", "rating", "created_at")
    list_filter = ("rating", "created_at", "book")
    search_fields = ("book__name", "reviewer__first_name",
                     "reviewer__last_name", "text")


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "event_date", "library")
    list_filter = ("library", "event_date")
    search_fields = ("title", "description")
    filter_horizontal = ("books",)


@admin.register(EventParticipant)
class EventParticipantAdmin(admin.ModelAdmin):
    list_display = ("event", "member", "registration_date")
    list_filter = ("event", "registration_date", "member")
    search_fields = ("event__title", "member__first_name", "member__last_name")


class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "short_title", "status", "deadline", "created_at")
    list_filter = ("status", "deadline", "created_at", "categories")
    search_fields = ("title", "description")
    filter_horizontal = ("categories",)
    ordering = ("-created_at",)
    inlines = [SubTaskInline]

    def short_title(self, obj):
        title = obj.title or ""
        return title[:10] + "..." if len(title) > 10 else title

    short_title.short_description = "Название"


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ("title", "task", "status", "deadline", "created_at")
    list_filter = ("status", "deadline", "created_at", "task")
    search_fields = ("title", "description", "task__title")
    ordering = ("-created_at",)
    actions = ["mark_as_done"]

    def mark_as_done(self, request, queryset):
        updated = queryset.update(status="done")
        self.message_user(request, f"Переведено в Done: {updated} подзадач.")

    mark_as_done.short_description = "Перевести выбранные подзадачи в статус Done"


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


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "phone", "adress")
    search_fields = ("name", "email", "phone")
    list_filter = ("name",)
