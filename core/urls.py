"""
URL configuration for core project.
"""

from django.contrib import admin
from django.urls import path, include

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# --- Swagger / drf-yasg ---
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Документация",
        default_version='v1',
        description="Проба вывода документации",

        # расширенные данные , разобраться позже, вставить в проект?

        # terms_of_service="https://www.google.com/policies/terms/",
        # contact=openapi.Contact(email="contact@local.com"),
        # license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [

    path('admin/', admin.site.urls),


    path('', include('app.urls')),
    path('', include('library.urls')),
    path('', include('Meta_Admin.urls')),


    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),


    path('api/auth/', include([
        path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ])),


    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),


    path(
        'redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),



]
