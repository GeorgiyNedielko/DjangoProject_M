from rest_framework.pagination import CursorPagination

class DefaultCursorPagination(CursorPagination):
    page_size = 5                      # по умолчанию 5 объектов
    ordering = "-created_at"           # сортировка по созданию (новые сверху)
    cursor_query_param = 'cursor'      # параметр курсора в URL
