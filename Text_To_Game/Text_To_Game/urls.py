# chaotix/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('image_generator/', include('image_generator.urls')),
]
