from django.urls import path
from . import api_views

urlpatterns = [
    path("api/books/", api_views.book_list_create, name="book-list-create"),
    path("api/books/<int:pk>/", api_views.book_detail, name="book-detail"),
]
