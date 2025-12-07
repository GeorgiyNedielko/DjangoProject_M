# library/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api_views import (
    book_list_create,
    book_detail_update_delete,
    GenreViewSet,
    CategoryViewSet,
)

router = DefaultRouter()
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('api/books/', book_list_create, name='book-list-create'),
    path('api/books/<int:pk>/', book_detail_update_delete, name='book-detail-update-delete'),
    path('api/', include(router.urls)),
]
