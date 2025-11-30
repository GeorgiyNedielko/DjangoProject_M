from rest_framework import serializers
from .models import Book


class BookListSerializer(serializers.ModelSerializer):
    """Краткая информация о книге для списка"""
    author = serializers.StringRelatedField()
    publisher = serializers.StringRelatedField()
    category = serializers.StringRelatedField()
    library = serializers.StringRelatedField()

    class Meta:
        model = Book
        fields = (
            "id",
            "name",
            "author",
            "publisher",
            "category",
            "library",
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

    class Meta:
        model = Book
        fields = "__all__"


class BookCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания/обновления книги.
    created_at заполняется автоматически (или через сигнал/логика),
    поэтому его не даём изменять через API.
    """

    class BookCreateSerializer(serializers.ModelSerializer):
        discounted_price = serializers.DecimalField(
            max_digits=10, decimal_places=2, write_only=True, required=False
        )

    class Meta:
        model = Book
        fields = '__all__'


