"""
URL configuration for library_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.shortcuts import redirect
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator

class PublicSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        """Generate schema without authentication requirements."""
        schema = super().get_schema(request, public=True)
        # Remove security requirements from all operations
        for path in schema.get('paths', {}).values():
            for operation in path.values():
                if isinstance(operation, dict):
                    operation.pop('security', None)
                    # Also remove any authentication-related parameters
                    if 'parameters' in operation:
                        operation['parameters'] = [p for p in operation['parameters'] 
                                                 if p.get('name') not in ['Authorization', 'authorization']]
        # Remove global security definitions
        schema.pop('securityDefinitions', None)
        schema.pop('security', None)
        return schema

# Public schema view for documentation (no authentication required)
public_schema_view = get_schema_view(
   openapi.Info(
      title="Library Management API",
      default_version='v1',
      description="A comprehensive API for managing a library system. Note: API endpoints require authentication, but this documentation is publicly accessible.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@library.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   generator_class=PublicSchemaGenerator,
   authentication_classes=[],
)

# Private schema view for authenticated access
schema_view = get_schema_view(
   openapi.Info(
      title="Library Management API",
      default_version='v1',
      description="A comprehensive API for managing a library system with authentication and role-based permissions",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@library.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', lambda request: redirect('/swagger/'), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/', include('library.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', public_schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', public_schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', public_schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
