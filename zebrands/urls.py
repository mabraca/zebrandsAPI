"""
URL configuration for zebrands project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls.py import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls.py'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

"""
Swagger documentation setup
"""
schema_view = get_schema_view(
    openapi.Info(
        title="Zebrands API",
        default_version='v1',
        description="This project is an API REST for a product catalog. If you want change something or ask "
                    "why you can contact to me by email",
        contact=openapi.Contact(email="mabraca18@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

"""
127.0.0.1:8000/admin For adminstration user and product in Django
127.0.0.1:8000/api For API REST method PUT/DELETE/ADD is just allow with admin users
127.0.0.1:8000/ To see basic web page connected with API REST
"""
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('catalog_api.urls')),
    path('', include('catalog_web.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
