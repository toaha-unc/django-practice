from django.db import models
from django.utils import timezone


class Author(models.Model):
    """Model representing an author of books."""
    name = models.CharField(max_length=200)
    biography = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    """Model representing a book in the library."""
    CATEGORY_CHOICES = [
        ('fiction', 'Fiction'),
        ('non-fiction', 'Non-Fiction'),
        ('science', 'Science'),
        ('technology', 'Technology'),
        ('history', 'History'),
        ('biography', 'Biography'),
        ('philosophy', 'Philosophy'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
    ]

    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    isbn = models.CharField(max_length=13, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    availability_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return f"{self.title} by {self.author.name}"


class Member(models.Model):
    """Model representing a library member."""
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    membership_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.name} ({self.email})"


class BorrowRecord(models.Model):
    """Model representing a book borrowing record."""
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrow_records')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='borrow_records')
    borrow_date = models.DateTimeField(default=timezone.now)
    return_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.book.title} borrowed by {self.member.name} on {self.borrow_date.date()}"

    def save(self, *args, **kwargs):
        # Update book availability status when borrowing/returning
        if not self.pk:  # New record
            self.book.availability_status = 'borrowed'
            self.book.save()
        elif self.return_date:
            self.book.availability_status = 'available'
            self.book.save()
        
        super().save(*args, **kwargs)
