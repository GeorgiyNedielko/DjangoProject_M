# library/api_views.py

from rest_framework import status, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.db.models import Count

from .models import Book, Genre, Category
from .serializers import (
    BookListSerializer,
    BookDetailSerializer,
    BookCreateUpdateSerializer,
    GenreSerializer,
    CategorySerializer,
)

# ===== КНИГИ =====

@api_view(['GET', 'POST'])
def book_list_create(request):
    """GET -> список книг, POST -> создать книгу"""
    if request.method == 'GET':
        qs = Book.objects.all().order_by("-id")
        serializer = BookListSerializer(qs, many=True)
        return Response(serializer.data)

    serializer = BookCreateUpdateSerializer(data=request.data)
    if serializer.is_valid():
        book = serializer.save()
        return Response(BookDetailSerializer(book).data, status=201)

    return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def book_detail_update_delete(request, pk):
    """CRUD для одной книги"""
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response({'error': 'Book not found'}, status=404)

    if request.method == 'GET':
        return Response(BookDetailSerializer(book).data)

    elif request.method == 'PUT':
        serializer = BookCreateUpdateSerializer(book, data=request.data)
        if serializer.is_valid():
            book = serializer.save()
            return Response(BookDetailSerializer(book).data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        book.delete()
        return Response(status=204)


# ===== ЖАНРЫ =====

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    @action(detail=False, methods=['get'])
    def statistic(self, request):
        """GET /api/genres/statistic/ — жанры + количество книг"""
        genres = Genre.objects.annotate(book_count=Count('books')).order_by('name')
        return Response(self.get_serializer(genres, many=True).data)


# ===== КАТЕГОРИИ =====

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=False, methods=['get'], url_path="count-tasks")
    def count_tasks(self, request):
        """Категории + количество задач"""
        data = Category.objects.annotate(
            tasks_count=Count("tasks")
        ).values("id", "name", "tasks_count")

        return Response(list(data))
