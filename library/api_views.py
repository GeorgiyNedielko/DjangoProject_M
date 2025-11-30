# library/api_views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Book
from .serializers import (
    BookListSerializer,
    BookDetailSerializer,
    BookCreateUpdateSerializer,
)


@api_view(['GET', 'POST'])
def book_list_create(request):
    """
    GET  /api/books/  -> список всех книг (краткий сериализатор)
    POST /api/books/  -> создание новой книги
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
    GET    /api/books/<pk>/  -> одна книга (полная инфа)
    PUT    /api/books/<pk>/  -> полное обновление
    DELETE /api/books/<pk>/  -> удаление
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
            # снова отдаём детальную инфу
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