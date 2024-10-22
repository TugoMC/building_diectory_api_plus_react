from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authapp.api_urls')),
    path('api/professionals/', include('professionals.api_urls')),
]