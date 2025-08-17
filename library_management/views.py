from django.http import HttpResponse
from django.template import Template, Context
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

@method_decorator(csrf_exempt, name='dispatch')
class PublicSwaggerView(View):
    """Custom Swagger view that serves documentation without authentication."""
    
    def get(self, request):
        from django.template.loader import render_to_string
        return HttpResponse(render_to_string('swagger-ui.html'), content_type='text/html')
