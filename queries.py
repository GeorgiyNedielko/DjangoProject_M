import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# from test_app.models import (
#     Book,
#     UserProfile
# )


# try:
#     book = Book.objects.get(author="Leo Tolstoy")  # MultipleObjectsReturned
#     # book = Book.objects.get(id=999999999)  # DoesNotExist
#
#     print(book)
# except Book.DoesNotExist as err:
#     print("Нет такой книги", err)
# except Book.MultipleObjectsReturned as err:
#     print("Слишком много книг найдено", err)


# leo_books = Book.objects.filter(author="Leo Tolstoy")
#
# print(leo_books.query)
# print(leo_books)


# __contains == частичное совпадение с учётом регистра
# __icontains == частичное совпадение БЕЗ учёта регистра
# i == ignore_case

# leo_books = Book.objects.filter(title__contains="P")
#
# print(leo_books.query)
# print(leo_books)



# books = Book.objects.filter(id__in=[15, 280, 361])
#
# print(books.query)
#
# for b in books:
#     print(b.id, b.title)


# books = Book.objects.filter(pages__gt=500)
#
# print(books.query)
#
# for b in books:
#     print(b.id, b.title)


# filter(<field_name>__<lookups_name>)
# books = Book.objects.filter(published_date__gte="2020-01-01")
#
# print(books.query)
#
# for b in books:
#     print(b.id, b.published_date)


# books = Book.objects.filter(pages__isnull=True)
#
# print(books.query)
#
# for b in books:
#     print(b.id, b.published_date)


# books = Book.objects.filter(title__startswith="A")
#
# print(books.query)
#
# for b in books:
#     print(b.id, b.published_date)


# books = Book.objects.filter(pages__range=[<start>, <stop>])
# books = Book.objects.filter(pages__range=[500, 700])
#
# print(books.query)
#
# for b in books:
#     print(f"{b.id=}  -- {b.pages=}")


#
# books = Book.objects.filter(
#     pages__range=[500, 700],
#     published_date__gte='2020-01-01'
# )
#
# print(books.query)
#
# for b in books:
#     print(f"{b.id=}  -- {b.pages=}")



# =====================================================================

# from django.db.models import Q

# Q class

# OR - |
# AND - &
# NOT - ~

# data = Book.objects.filter(
#     Q(Q(author__startswith="Fyodor") | Q(author__startswith="Jack")) & Q(published_date__gte='2015-05-31')
# )
#
# print(data.query)
#
# for b in data:  # type: Book
#     print(f"{b.id=}  --  {b.author}  --  {b.published_date}")


# """
# SELECT
#     "books"."id",
#     "books"."title",
#     "books"."description",
#     "books"."author",
#     "books"."published_date",
#     "books"."pages"
# FROM "books"
# WHERE (
#           ("books"."author" LIKE Fyodor% ESCAPE '\'
#           OR "books"."author" LIKE Jack% ESCAPE '\'
#           )
#               AND "books"."published_date" >= 2015-05-31
#       )
# ORDER BY "books"."published_date" ASC
#
# """


# data = Book.objects.filter(
#     Q(
#         Q(author__startswith="Fyodor") | Q(Q(author__startswith="Jack") & ~Q(author__endswith="London"))
#     ) & Q(published_date__gte='2015-05-31')
# )
#
# print(data.query)
#
# for b in data:  # type: Book
#     print(f"{b.id=}  --  {b.author}  --  {b.published_date}")

from decimal import Decimal

# book = Book.objects.get(id=700)
#
# print("BEFORE:")
# print(book.is_bestseller)
# print(book.price)
#
#
# book.is_bestseller = True
# book.price = Decimal("189.97")
#
# book.save()
# print("AFTER:")
# print(book.is_bestseller)
# print(book.price)


# books = Book.objects.filter(
#     author__in=["Leo Tolstoy", "Fyodor Dostoevsky"]
# ).update(is_bestseller=True, price=Decimal("299.99"))
#


# from django.db.models import F
#
#
# books = Book.objects.filter(
#     author__in=["Leo Tolstoy", "Fyodor Dostoevsky"]
# ).update(discounted_price=F('price') * 0.80)



# book_to_delete = Book.objects.get(id=720)
#
#
# book_to_delete.delete()
#
#
#
# Book.objects.create()
# Book.objects.bulk_create()
# Book.objects.bulk_update()

