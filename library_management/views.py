from django.http import HttpResponse
from django.template import Template, Context
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework import settings as drf_settings # Imported for temporary override

@method_decorator(csrf_exempt, name='dispatch')
class PublicSwaggerView(View):
    """Custom Swagger view that serves documentation without authentication."""
    
    def get(self, request):
        # Create Swagger UI HTML that points to the schema endpoint
        swagger_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Library Management API</title>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" type="text/css" href="/static/drf-yasg/swagger-ui-dist/swagger-ui.css">
    <style>
        /* Hide all authentication-related elements */
        .authorize-wrapper,
        .btn.authorize,
        .auth-wrapper,
        .auth-container,
        [data-sw-translate="authorize"],
        .swagger-ui .auth-wrapper,
        .swagger-ui .authorize-wrapper,
        .swagger-ui .authorize {
            display: none !important;
        }
        
        /* Hide any login-related elements */
        .swagger-ui .auth-btn,
        .swagger-ui .login-btn {
            display: none !important;
        }
    </style>
</head>
<body>
    <div id="swagger-ui"></div>
    <script src="/static/drf-yasg/swagger-ui-dist/swagger-ui-bundle.js"></script>
    <script src="/static/drf-yasg/swagger-ui-dist/swagger-ui-standalone-preset.js"></script>
    <script>
        window.onload = function() {
            const ui = SwaggerUIBundle({
                url: '/swagger/?format=openapi',
                dom_id: '#swagger-ui',
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIStandalonePreset
                ],
                layout: "StandaloneLayout",
                deepLinking: true,
                showExtensions: true,
                showCommonExtensions: true,
                docExpansion: "list",
                defaultModelRendering: "model",
                defaultModelsExpandDepth: 3,
                defaultModelExpandDepth: 3,
                displayOperationId: true,
                persistAuthorization: false,
                refetchWithAuth: false,
                refetchOnLogout: false,
                fetchSchemaWithQuery: true,
                onComplete: function() {
                    // Hide any remaining auth elements after the UI loads
                    const authElements = document.querySelectorAll(
                        '.authorize-wrapper, .btn.authorize, [data-sw-translate="authorize"], ' +
                        '.auth-wrapper, .auth-container, .swagger-ui .authorize, ' +
                        '.swagger-ui .auth-btn, .swagger-ui .login-btn'
                    );
                    authElements.forEach(el => {
                        el.style.display = 'none';
                        el.remove();
                    });
                    
                    // Also hide any elements with "login" in their text
                    const allElements = document.querySelectorAll('*');
                    allElements.forEach(el => {
                        if (el.textContent && el.textContent.toLowerCase().includes('django login')) {
                            el.style.display = 'none';
                            el.remove();
                        }
                    });
                }
            });
        };
    </script>
</body>
</html>
        """
        
        return HttpResponse(swagger_html, content_type='text/html')
