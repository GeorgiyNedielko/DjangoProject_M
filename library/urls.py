# library/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api_views import (
    book_list_create,
    book_detail_update_delete,
    GenreViewSet, CategoryViewSet
)

router = DefaultRouter()
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r"categories", CategoryViewSet, basename="category")

urlpatterns = [
    # Книги (функциональные вьюхи)
    path('books/', book_list_create, name='book-list-create'),
    path('books/<int:pk>/', book_detail_update_delete, name='book-detail-update-delete'),

    # Жанры (ViewSet через DRF router)
    path('api/', include(router.urls)),
]
