from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from library.models import Author, Book
import json

@csrf_exempt
def setup_database(request):
    """Vercel function to set up database and create users."""
    if request.method == 'POST':
        try:
            # Create admin user
            admin_user, created = User.objects.get_or_create(
                username='admin',
                defaults={
                    'email': 'admin@library.com',
                    'first_name': 'Admin',
                    'last_name': 'User',
                    'is_staff': True,
                    'is_superuser': True,
                }
            )
            
            if created:
                admin_user.set_password('adminadmin')
                admin_user.save()
                admin_message = "Admin user created successfully"
            else:
                admin_user.set_password('adminadmin')
                admin_user.save()
                admin_message = "Admin user password updated"

            # Create sample authors
            authors_data = [
                {'name': 'J.K. Rowling', 'biography': 'British author best known for the Harry Potter series'},
                {'name': 'George R.R. Martin', 'biography': 'American novelist and short story writer'},
                {'name': 'Stephen King', 'biography': 'American author of horror, supernatural fiction, suspense, and fantasy novels'},
            ]

            authors_created = 0
            for author_data in authors_data:
                author, created = Author.objects.get_or_create(
                    name=author_data['name'],
                    defaults={'biography': author_data['biography']}
                )
                if created:
                    authors_created += 1

            # Create sample books
            books_created = 0
            if authors_created > 0:
                books_data = [
                    {'title': 'Harry Potter and the Philosopher\'s Stone', 'author': authors[0], 'isbn': '9780747532699', 'category': 'fiction'},
                    {'title': 'A Game of Thrones', 'author': authors[1], 'isbn': '9780553103540', 'category': 'fiction'},
                ]

                for book_data in books_data:
                    book, created = Book.objects.get_or_create(
                        isbn=book_data['isbn'],
                        defaults={
                            'title': book_data['title'],
                            'author': book_data['author'],
                            'category': book_data['category'],
                        }
                    )
                    if created:
                        books_created += 1

            return JsonResponse({
                'success': True,
                'message': 'Database setup completed successfully',
                'admin_user': admin_message,
                'authors_created': authors_created,
                'books_created': books_created,
                'credentials': {
                    'username': 'admin',
                    'password': 'adminadmin'
                }
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

    return JsonResponse({
        'success': False,
        'error': 'Only POST method allowed'
    }, status=405)
