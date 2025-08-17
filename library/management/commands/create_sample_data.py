from django.core.management.base import BaseCommand
from library.models import Author, Book, Member, BorrowRecord


class Command(BaseCommand):
    help = 'Create sample data for the library system'

    def handle(self, *args, **options):
        # Create authors
        authors_data = [
            {'name': 'J.K. Rowling', 'biography': 'British author best known for the Harry Potter series'},
            {'name': 'George R.R. Martin', 'biography': 'American novelist and short story writer'},
            {'name': 'Stephen King', 'biography': 'American author of horror, supernatural fiction, suspense, and fantasy novels'},
            {'name': 'Agatha Christie', 'biography': 'English writer known for her detective novels'},
            {'name': 'Ernest Hemingway', 'biography': 'American novelist, short story writer, and journalist'},
        ]

        authors = []
        for author_data in authors_data:
            author, created = Author.objects.get_or_create(
                name=author_data['name'],
                defaults={'biography': author_data['biography']}
            )
            authors.append(author)
            if created:
                self.stdout.write(f'Created author: {author.name}')

        # Create books
        books_data = [
            {'title': 'Harry Potter and the Philosopher\'s Stone', 'author': authors[0], 'isbn': '9780747532699', 'category': 'fiction'},
            {'title': 'A Game of Thrones', 'author': authors[1], 'isbn': '9780553103540', 'category': 'fiction'},
            {'title': 'The Shining', 'author': authors[2], 'isbn': '9780385121675', 'category': 'fiction'},
            {'title': 'Murder on the Orient Express', 'author': authors[3], 'isbn': '9780062073495', 'category': 'fiction'},
            {'title': 'The Old Man and the Sea', 'author': authors[4], 'isbn': '9780684801223', 'category': 'fiction'},
            {'title': 'Harry Potter and the Chamber of Secrets', 'author': authors[0], 'isbn': '9780747538493', 'category': 'fiction'},
            {'title': 'A Clash of Kings', 'author': authors[1], 'isbn': '9780553108033', 'category': 'fiction'},
            {'title': 'Carrie', 'author': authors[2], 'isbn': '9780385086950', 'category': 'fiction'},
        ]

        books = []
        for book_data in books_data:
            book, created = Book.objects.get_or_create(
                isbn=book_data['isbn'],
                defaults={
                    'title': book_data['title'],
                    'author': book_data['author'],
                    'category': book_data['category'],
                }
            )
            books.append(book)
            if created:
                self.stdout.write(f'Created book: {book.title}')

        # Get the member we created earlier
        try:
            member = Member.objects.get(user__username='member')
            self.stdout.write(f'Found member: {member.name}')
        except Member.DoesNotExist:
            self.stdout.write(self.style.ERROR('Member not found. Please run create_test_users first.'))
            return

        # Create some borrow records
        borrow_records_data = [
            {'book': books[0], 'member': member},  # Harry Potter borrowed
            {'book': books[2], 'member': member},  # The Shining borrowed
        ]

        for record_data in borrow_records_data:
            record, created = BorrowRecord.objects.get_or_create(
                book=record_data['book'],
                member=record_data['member'],
                return_date__isnull=True,
                defaults={}
            )
            if created:
                self.stdout.write(f'Created borrow record: {record.book.title} borrowed by {record.member.name}')

        self.stdout.write(
            self.style.SUCCESS('Sample data created successfully!')
        )
