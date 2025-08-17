from rest_framework import serializers
from .models import Author, Book, Member, BorrowRecord


class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for the Author model."""
    class Meta:
        model = Author
        fields = ['id', 'name', 'biography']


class BookSerializer(serializers.ModelSerializer):
    """Serializer for the Book model."""
    author_name = serializers.CharField(source='author.name', read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'author_name', 'isbn', 'category', 'availability_status']


class MemberSerializer(serializers.ModelSerializer):
    """Serializer for the Member model."""
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Member
        fields = ['id', 'user', 'username', 'name', 'email', 'membership_date']


class BorrowRecordSerializer(serializers.ModelSerializer):
    """Serializer for the BorrowRecord model."""
    book_title = serializers.CharField(source='book.title', read_only=True)
    member_name = serializers.CharField(source='member.name', read_only=True)

    class Meta:
        model = BorrowRecord
        fields = ['id', 'book', 'book_title', 'member', 'member_name', 'borrow_date', 'return_date']


class BorrowBookSerializer(serializers.Serializer):
    """Serializer for borrowing a book."""
    book_id = serializers.IntegerField()
    member_id = serializers.IntegerField()


class ReturnBookSerializer(serializers.Serializer):
    """Serializer for returning a book."""
    borrow_record_id = serializers.IntegerField()
