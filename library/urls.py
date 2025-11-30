from django.urls import path
from .api_views import book_list_create, book_detail_update_delete

urlpatterns = [
    path('books/', book_list_create, name='book-list-create'),
    path('books/<int:pk>/', book_detail_update_delete, name='book-detail-update-delete'),
]
