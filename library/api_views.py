# library/api_views.py

from rest_framework import status, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Book, Genre, Category
from .serializers import (
    BookListSerializer,
    BookDetailSerializer,
    BookCreateUpdateSerializer,
    GenreSerializer, CategorySerializer
)
from django.db.models import Count


# ===== КНИГИ (функциональные вьюхи) =====

@api_view(['GET', 'POST'])
def book_list_create(request):
    """
    GET  /books/        -> список всех книг (краткий сериализатор)
    POST /books/        -> создание новой книги
    """
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookListSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = BookCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            book = serializer.save()
            return Response(
                BookDetailSerializer(book).data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def book_detail_update_delete(request, pk):
    """
    GET    /books/<pk>/  -> одна книга (полная инфа)
    PUT    /books/<pk>/  -> полное обновление
    DELETE /books/<pk>/  -> удаление
    """
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response(
            {'error': 'Book not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        serializer = BookDetailSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = BookCreateUpdateSerializer(book, data=request.data)
        if serializer.is_valid():
            book = serializer.save()
            return Response(
                BookDetailSerializer(book).data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    elif request.method == 'DELETE':
        book.delete()
        return Response(
            {'message': 'Book deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )


# ===== ЖАНРЫ (ViewSet) =====

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    @action(detail=False, methods=['get'])
    def statistic(self, request):
        """
        GET /api/genres/statistic/
        Возвращает жанры с количеством книг в каждом.
        """
        genres = Genre.objects.annotate(
            book_count=Count('books')  # related_name='books' у Book.genre
        ).order_by('name')

        serializer = self.get_serializer(genres, many=True)
        return Response(serializer.data)

class CategoryViewSet(ModelViewSet):
    """
    Полный CRUD для категорий с soft delete.
    destroy() будет вызывать наш переопределённый delete() в модели.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=False, methods=["get"], url_path="count-tasks")
    def count_tasks(self, request):
        """
        Вернёт список категорий с количеством задач в каждой:
        [
            {"id": 1, "name": "Bestsellers", "tasks_count": 3},
            ...
        ]
        """
        data = (
            Category.objects
            .annotate(tasks_count=Count("tasks"))  # Task.categories.related_name="tasks"
            .values("id", "name", "tasks_count")
        )
        return Response(list(data))