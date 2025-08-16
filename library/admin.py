from django.contrib import admin
from .models import Author, Book, Member, BorrowRecord


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'books_count']
    search_fields = ['name']

    def books_count(self, obj):
        return obj.books.count()
    books_count.short_description = 'Number of Books'


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'category', 'availability_status']
    list_filter = ['category', 'availability_status']
    search_fields = ['title', 'author__name', 'isbn']
    autocomplete_fields = ['author']


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'membership_date']
    list_filter = ['membership_date']
    search_fields = ['name', 'email']


@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ['book', 'member', 'borrow_date', 'return_date']
    list_filter = ['borrow_date']
    search_fields = ['book__title', 'member__name']
    autocomplete_fields = ['book', 'member']
