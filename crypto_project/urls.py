from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Your API endpoints
    path('accounts/', include('django.contrib.auth.urls')),  # Adds login, logout, password reset, etc.
]
