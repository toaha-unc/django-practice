from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.conf import settings
from django.templatetags.static import static

@method_decorator(csrf_exempt, name='dispatch')
class PublicSwaggerView(View):
    """Custom Swagger view that serves documentation without authentication."""
    
    def get(self, request):
        # Get the current domain for proper URL generation
        protocol = 'https' if request.is_secure() else 'http'
        domain = request.get_host()
        base_url = f"{protocol}://{domain}"
        
        # Create Swagger UI HTML using local static files with WhiteNoise
        swagger_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Library Management API</title>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" type="text/css" href="{base_url}/static/drf-yasg/swagger-ui-dist/swagger-ui.css">
    <style>
        /* Hide authentication elements for public documentation */
        .authorize-wrapper,
        .btn.authorize,
        .auth-wrapper,
        .auth-container,
        [data-sw-translate="authorize"],
        .swagger-ui .auth-wrapper,
        .swagger-ui .authorize-wrapper,
        .swagger-ui .authorize {{
            display: none !important;
        }}
        
        /* Hide any login-related elements */
        .swagger-ui .auth-btn,
        .swagger-ui .login-btn {{
            display: none !important;
        }}
        
        /* Add some custom styling */
        .swagger-ui .topbar {{
            display: none;
        }}
        
        .swagger-ui .info {{
            margin: 20px 0;
        }}
        
        /* Ensure proper loading */
        body {{
            margin: 0;
            padding: 20px;
            background: #fafafa;
        }}
        
        #swagger-ui {{
            max-width: 1200px;
            margin: 0 auto;
        }}
    </style>
</head>
<body>
    <div id="swagger-ui"></div>
    <script src="{base_url}/static/drf-yasg/swagger-ui-dist/swagger-ui-bundle.js"></script>
    <script src="{base_url}/static/drf-yasg/swagger-ui-dist/swagger-ui-standalone-preset.js"></script>
    <script>
        window.onload = function() {{
            console.log('Loading Swagger UI...');
            
            const ui = SwaggerUIBundle({{
                url: '{base_url}/swagger/?format=openapi',
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
                onComplete: function() {{
                    console.log('Swagger UI loaded successfully');
                    // Hide any remaining auth elements after the UI loads
                    const authElements = document.querySelectorAll(
                        '.authorize-wrapper, .btn.authorize, [data-sw-translate="authorize"], ' +
                        '.auth-wrapper, .auth-container, .swagger-ui .authorize, ' +
                        '.swagger-ui .auth-btn, .swagger-ui .login-btn'
                    );
                    authElements.forEach(el => {{
                        el.style.display = 'none';
                        el.remove();
                    }});
                }},
                onError: function(error) {{
                    console.error('Swagger UI error:', error);
                    document.getElementById('swagger-ui').innerHTML = 
                        '<h1>Error loading Swagger UI: ' + error.message + '</h1>';
                }}
            }});
        }};
    </script>
</body>
</html>
        """
        
        return HttpResponse(swagger_html, content_type='text/html')
