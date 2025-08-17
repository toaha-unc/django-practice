from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone

from .models import Author, Book, Member, BorrowRecord
from .serializers import (
    AuthorSerializer, BookSerializer, MemberSerializer, 
    BorrowRecordSerializer, BorrowBookSerializer, ReturnBookSerializer
)
from .permissions import IsLibrarianOrReadOnly, IsLibrarianOrMemberReadOnly, IsLibrarian


class AuthorViewSet(viewsets.ModelViewSet):
    """ViewSet for managing authors."""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsLibrarianOrReadOnly]


class BookViewSet(viewsets.ModelViewSet):
    """ViewSet for managing books."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsLibrarianOrReadOnly]


class MemberViewSet(viewsets.ModelViewSet):
    """ViewSet for managing members."""
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsLibrarian]


class BorrowRecordViewSet(viewsets.ModelViewSet):
    """ViewSet for managing borrowing records."""
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer
    permission_classes = [IsLibrarianOrMemberReadOnly]

    @action(detail=False, methods=['post'])
    def borrow(self, request):
        """Borrow a book."""
        serializer = BorrowBookSerializer(data=request.data)
        if serializer.is_valid():
            book_id = serializer.validated_data['book_id']
            member_id = serializer.validated_data['member_id']
            
            try:
                book = Book.objects.get(id=book_id)
                member = Member.objects.get(id=member_id)
                
                if book.availability_status != 'available':
                    return Response(
                        {'error': 'Book is not available for borrowing.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                borrow_record = BorrowRecord.objects.create(
                    book=book,
                    member=member
                )
                
                borrow_serializer = BorrowRecordSerializer(borrow_record)
                return Response(borrow_serializer.data, status=status.HTTP_201_CREATED)
                
            except (Book.DoesNotExist, Member.DoesNotExist):
                return Response(
                    {'error': 'Book or member not found.'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def return_book(self, request):
        """Return a borrowed book."""
        serializer = ReturnBookSerializer(data=request.data)
        if serializer.is_valid():
            borrow_record_id = serializer.validated_data['borrow_record_id']
            
            try:
                borrow_record = BorrowRecord.objects.get(id=borrow_record_id)
                
                if borrow_record.return_date:
                    return Response(
                        {'error': 'Book has already been returned.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                borrow_record.return_date = timezone.now()
                borrow_record.save()
                
                borrow_serializer = BorrowRecordSerializer(borrow_record)
                return Response(borrow_serializer.data, status=status.HTTP_200_OK)
                
            except BorrowRecord.DoesNotExist:
                return Response(
                    {'error': 'Borrowing record not found.'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
