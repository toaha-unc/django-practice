#!/usr/bin/env python
"""
Test database connection for deployed Django application.
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_management.settings')
django.setup()

from django.db import connection
from django.contrib.auth.models import User

def test_database_connection():
    """Test if database connection works."""
    try:
        # Test basic connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print(f"✅ Database connection successful: {result}")
        
        # Test User model
        user_count = User.objects.count()
        print(f"✅ User model accessible. Total users: {user_count}")
        
        # List existing users
        users = User.objects.all()
        print("📋 Existing users:")
        for user in users:
            print(f"  - {user.username} (staff: {user.is_staff}, superuser: {user.is_superuser})")
            
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == '__main__':
    print("🔍 Testing database connection...")
    test_database_connection()
