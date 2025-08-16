#!/usr/bin/env python3
"""
Test script for the Library Management System API
"""

import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_api():
    print("Testing Library Management System API")
    print("=" * 50)
    
    print("\n1. Creating an author...")
    author_data = {
        "name": "J.K. Rowling",
        "biography": "British author best known for the Harry Potter series."
    }
    
    response = requests.post(f"{BASE_URL}/authors/", json=author_data)
    if response.status_code == 201:
        author = response.json()
        print(f"Author created: {author['name']} (ID: {author['id']})")
        author_id = author['id']
    else:
        print(f"Failed to create author: {response.text}")
        return
    
    print("\n2. Creating a book...")
    book_data = {
        "title": "Harry Potter and the Philosopher's Stone",
        "author": author_id,
        "isbn": "9780747532699",
        "category": "fiction",
        "publication_year": 1997,
        "description": "The first book in the Harry Potter series."
    }
    
    response = requests.post(f"{BASE_URL}/books/", json=book_data)
    if response.status_code == 201:
        book = response.json()
        print(f"Book created: {book['title']} (ID: {book['id']})")
        book_id = book['id']
    else:
        print(f"Failed to create book: {response.text}")
        return

    print("\n3. Listing all books...")
    response = requests.get(f"{BASE_URL}/books/")
    if response.status_code == 200:
        books = response.json()
        print(f"Found {len(books)} books:")
        for book in books:
            print(f"   - {book['title']} by {book['author_name']}")
    else:
        print(f"Failed to list books: {response.text}")
    

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API server.")
        print("Make sure the Django development server is running:")
        print("  python manage.py runserver")
    except Exception as e:
        print(f"Error: {e}")
