from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.db.models import Avg

class Author(models.Model):
    name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Отображаемое имя",
    )

    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    birth_date = models.DateField(verbose_name="Дата рождения")

    profile = models.URLField(
        blank=True,
        null=True,
        verbose_name="Профиль автора"
    )

    is_deleted = models.BooleanField(
        default=False,
        verbose_name="Удаленный",
        help_text="Если False - автор активен. Если True - автора больше нет в списке доступных",
    )

    rating = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Рейтинг",
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class AuthorDetail(models.Model):
    # Связь с моделью Author (1 к 1 — у автора может быть только одна карточка с деталями)
    author = models.OneToOneField(
        'Author',
        on_delete=models.CASCADE,
        related_name='details',
        verbose_name='Автор'
    )

    biography = models.TextField(
        'Биография'
    )

    birth_city = models.CharField(
        'Город рождения',
        max_length=100,
        null=True,
        blank=True          # необязательное поле
    )

    GENDERS = (
        ('male', 'Мужской'),
        ('female', 'Женский'),
        ('other', 'Другой'),
    )

    gender = models.CharField(
        'Гендер',
        max_length=10,
        choices=GENDERS
    )

    class Meta:
        verbose_name = 'Доп. данные автора'
        verbose_name_plural = 'Доп. данные авторов'

    def __str__(self):
        return f'Данные об авторе: {self.author}'



class Category(models.Model):
    name = models.CharField('Название категории', max_length=100, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


STATUS_CHOICES = [
    ('new', 'New'),
    ('in_progress', 'In progress'),
    ('pending', 'Pending'),
    ('blocked', 'Blocked'),
    ('done', 'Done'),
]

class Library(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название библиотеки")
    location = models.CharField(max_length=200, verbose_name="Адрес")
    site = models.URLField(null=True, blank=True, verbose_name="Сайт")

    def __str__(self):
        return self.name

class Member(models.Model):
    GENDER_CHOICES = [
        ('male', 'Мужской'),
        ('female', 'Женский'),
    ]
    ROLE_CHOICES = [
        ('admin', 'Админ'),
        ('staff', 'Сотрудник'),
        ('reader', 'Читатель'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    gender = models.CharField(max_length=100, choices=GENDER_CHOICES)

    birth_date = models.DateField()
    age = models.IntegerField(
        validators=[
            MinValueValidator(6),
            MaxValueValidator(120)
        ]
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    active = models.BooleanField(default=True)

    libraries = models.ManyToManyField(
        'Library',
        related_name='members'
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Posts(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Оглавление",
    )

    text = models.TextField(
        verbose_name="Текст поста",
    )

    author = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Автор",
    )

    is_moderated = models.BooleanField(
        default=False,
        verbose_name="Промодерировано",
    )

    library = models.ForeignKey(
        Library,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Библиотека",
    )

    created_at = models.DateField(
        verbose_name="Дата создания",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления",
    )

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

        unique_together = ('title', 'created_at')

    def __str__(self):
        return self.title

class Borrow(models.Model):
    member = models.ForeignKey(
        "Member",
        on_delete=models.CASCADE,
        related_name='borrows',
        verbose_name='Член библиотеки',
    )

    book = models.ForeignKey(
        "Book",
        on_delete=models.CASCADE,
        related_name='borrows',
        verbose_name='Книга',
    )

    library = models.ForeignKey(
        "Library",
        on_delete=models.CASCADE,
        related_name='borrows',
        verbose_name='Библиотека',
    )

    borrow_date = models.DateField(
        verbose_name='Дата взятия книги',
    )

    return_date = models.DateField(
        verbose_name='Дата возврата книги',
    )

    is_returned = models.BooleanField(
        default=False,
        verbose_name='Книга возвращена',
    )

    class Meta:
        verbose_name = 'Выдача книги'
        verbose_name_plural = 'Выдачи книг'

    def __str__(self):
        return f'{self.member} — {self.book}'

    def is_overdue(self) -> bool:
        """
        Проверяет, просрочил ли читатель срок сдачи книги.
        Просрочка = сегодня позже даты возврата и книга ещё не возвращена.
        """
        if self.is_returned:
            return False

        today = timezone.localdate()
        return today > self.return_date

class Review(models.Model):
    book = models.ForeignKey(
        'Book',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Книга',
    )
    reviewer = models.ForeignKey(
        'Member',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Обозреватель',
    )
    rating = models.DecimalField(
        'Рейтинг',
        max_digits=2,
        decimal_places=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
        help_text='Оценка от 1.0 до 5.0',
    )
    text = models.TextField(
        'Отзыв',
    )
    created_at = models.DateTimeField(
        'Создано',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.book} – {self.reviewer} ({self.rating})'


class Book(models.Model):
    GENRE_CHOICES = [
        ('Fiction', 'Fiction'),
        ('Non-Fiction', 'Non-Fiction'),
        ('Science Fiction', 'Science Fiction'),
        ('Fantasy', 'Fantasy'),
        ('Mystery', 'Mystery'),
        ('Biography', 'Biography'),
    ]

    name = models.CharField(max_length=100, verbose_name="Имя книги")

    author = models.ForeignKey(
        Author,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="books",
        verbose_name="Автор",
    )

    publisher = models.ForeignKey(
        Member,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Публикатор",
        related_name="published_books",   #
    )

    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name="books"
    )

    library = models.ForeignKey(
        Library,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="books",
        verbose_name="Библиотека",
    )

    # ЭТУ строку УДАЛЯЕМ!
    # publisher_id = models.F(Member, null=True, on_delete=models.CASCADE)

    published_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Дата публикации"
    )

    description = models.TextField(
        blank=True,
        help_text="Краткое описание книги"
    )

    genre = models.CharField(
        max_length=50,
        choices=GENRE_CHOICES,
        null=True,
        blank=True,
        verbose_name="Жанр книги",
        help_text="Жанр книги",
    )

    pages = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(10000)],
        help_text="Количество страниц (максимум 10000)"
    )

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Цена",
    )
    publisher = models.ForeignKey('Publisher', on_delete=models.CASCADE,
                                  null=True, blank=True)

    def __str__(self):
        return  f"{self.name} by {self.author}"

    created_at = models.DateTimeField(null=True, blank=True)
    @property
    def rating(self):
        result = self.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
        return  float(result) if result is not None else 0.0

    def __str__(self):
        return self.name

from django.db import models




class Event(models.Model):
    title = models.CharField(
        'Название события',
        max_length=255
    )
    description = models.TextField(
        'Описание события'
    )
    event_date = models.DateTimeField(
        'Дата и время проведения'
    )
    library = models.ForeignKey(
        'Library',
        on_delete=models.CASCADE,
        related_name='events',
        verbose_name='Библиотека'
    )
    books = models.ManyToManyField(
        'Book',
        related_name='events',
        blank=True,
        verbose_name='Книги для обсуждения'
    )

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'
        ordering = ['-event_date']

    def __str__(self):

        return f'{self.title} ({self.event_date:%d.%m.%Y %H:%M})'

class EventParticipant(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='participants',
        verbose_name='Событие'
    )
    member = models.ForeignKey(
        'Member',
        on_delete=models.CASCADE,
        related_name='event_participations',
        verbose_name='Участник'
    )
    registration_date = models.DateField(
        'Дата регистрации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Участник события'
        verbose_name_plural = 'Участники событий'
        unique_together = ('event', 'member')

    def __str__(self):
        return f'{self.member} — {self.event}'


# ДЗ_8 (https://lms.itcareerhub.de/mod/assign/view.php?id=7551)


STATUS_CHOICES = [
    ('new', 'New'),
    ('in_progress', 'In progress'),
    ('pending', 'Pending'),
    ('blocked', 'Blocked'),
    ('done', 'Done'),
]


class Task(models.Model):
    title = models.CharField(
        'Название задачи',
        max_length=255,
        unique_for_date='created_at',
    )
    description = models.TextField('Описание задачи')
    categories = models.ManyToManyField(
        Category,
        related_name='tasks',
        verbose_name='Категории',
        blank=True,
    )
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
    )
    deadline = models.DateTimeField('Дедлайн')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['-created_at']

    def __str__(self):
        return self.title




class SubTask(models.Model):
    title = models.CharField('Название подзадачи', max_length=255)
    description = models.TextField('Описание подзадачи')
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='subtasks',
        verbose_name='Основная задача',
    )
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
    )
    deadline = models.DateTimeField('Дедлайн')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Подзадача'
        verbose_name_plural = 'Подзадачи'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} ({self.task})'

class Publisher(models.Model):
    name = models.CharField(max_length=100)
    established_date = models.DateField()

    def __str__(self):
        return self.name
