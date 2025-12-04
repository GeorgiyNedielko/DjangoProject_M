from rest_framework import serializers
from .models import Book, Category, Supplier, Genre


class BookListSerializer(serializers.ModelSerializer):
    """Краткая информация о книге для списка"""
    author = serializers.StringRelatedField()
    publisher = serializers.StringRelatedField()
    category = serializers.StringRelatedField()
    library = serializers.StringRelatedField()
    genre = serializers.StringRelatedField()

    class Meta:
        model = Book
        fields = (
            "id",
            "name",
            "author",
            "publisher",
            "category",
            "library",
            "genre",
            "price",
            "discounted_price",
            "is_bestseller",
        )


class BookDetailSerializer(serializers.ModelSerializer):
    """Полная информация о книге"""
    author = serializers.StringRelatedField()
    publisher = serializers.StringRelatedField()
    category = serializers.StringRelatedField()
    library = serializers.StringRelatedField()
    genre = serializers.StringRelatedField()

    class Meta:
        model = Book
        fields = "__all__"


class BookCreateUpdateSerializer(serializers.ModelSerializer):
    """Создание/обновление книги"""

    class Meta:
        model = Book
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"


class GenreSerializer(serializers.ModelSerializer):
    # ВОТ ЭТА СТРОКА ОБЯЗАТЕЛЬНА —
    # объявляем дополнительное поле, которого нет в модели
    book_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Genre
        fields = ["id", "name", "book_count"]
