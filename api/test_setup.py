from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import traceback

@csrf_exempt
def test_setup(request):
    """Test endpoint to check database connection and environment variables."""
    try:
        # Check environment variables
        env_vars = {
            'dbname': settings.DATABASES['default']['NAME'],
            'user': settings.DATABASES['default']['USER'],
            'host': settings.DATABASES['default']['HOST'],
            'port': settings.DATABASES['default']['PORT'],
            'password_set': 'YES' if settings.DATABASES['default']['PASSWORD'] else 'NO'
        }
        
        # Test database connection
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            db_test = f"Database connection successful: {result}"
            
        return JsonResponse({
            'success': True,
            'environment_variables': env_vars,
            'database_test': db_test,
            'debug_mode': settings.DEBUG
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc(),
            'environment_variables': {
                'dbname': getattr(settings.DATABASES['default'], 'NAME', 'NOT_SET'),
                'user': getattr(settings.DATABASES['default'], 'USER', 'NOT_SET'),
                'host': getattr(settings.DATABASES['default'], 'HOST', 'NOT_SET'),
                'port': getattr(settings.DATABASES['default'], 'PORT', 'NOT_SET'),
            }
        }, status=500)
