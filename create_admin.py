#!/usr/bin/env python
"""
Script to create admin user for deployed Django application.
Run this on the deployed server or locally with production settings.
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_management.settings')
django.setup()

from django.contrib.auth.models import User
from library.models import Author, Book, Member, BorrowRecord

def create_admin_user():
    """Create admin user if it doesn't exist."""
    try:
        # Check if admin user exists
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
            print("Admin user created successfully!")
            print("Username: admin")
            print("Password: adminadmin")
        else:
            # Update password if user exists
            admin_user.set_password('adminadmin')
            admin_user.save()
            print("Admin user password updated!")
            print("Username: admin")
            print("Password: adminadmin")
            
    except Exception as e:
        print(f"Error creating admin user: {e}")

def create_sample_data():
    """Create sample data if it doesn't exist."""
    try:
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
                print(f"Created author: {author.name}")

        # Create books
        books_data = [
            {'title': 'Harry Potter and the Philosopher\'s Stone', 'author': authors[0], 'isbn': '9780747532699', 'category': 'fiction'},
            {'title': 'A Game of Thrones', 'author': authors[1], 'isbn': '9780553103540', 'category': 'fiction'},
            {'title': 'The Shining', 'author': authors[2], 'isbn': '9780385121675', 'category': 'fiction'},
            {'title': 'Murder on the Orient Express', 'author': authors[3], 'isbn': '9780062073495', 'category': 'fiction'},
            {'title': 'The Old Man and the Sea', 'author': authors[4], 'isbn': '9780684801223', 'category': 'fiction'},
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
                print(f"Created book: {book.title}")

        print("Sample data created successfully!")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")

if __name__ == '__main__':
    print("Setting up Library Management System...")
    create_admin_user()
    create_sample_data()
    print("Setup completed!")
