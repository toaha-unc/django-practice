from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.contrib.auth.models import User

@csrf_exempt
def test_database(request):
    """Test database connection."""
    try:
        # Test basic connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            
        # Test User model
        user_count = User.objects.count()
        
        # List existing users
        users = list(User.objects.values('username', 'is_staff', 'is_superuser'))
        
        return JsonResponse({
            'success': True,
            'database_connection': 'OK',
            'user_count': user_count,
            'users': users,
            'test_query_result': result[0] if result else None
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'error_type': type(e).__name__
        }, status=500)
