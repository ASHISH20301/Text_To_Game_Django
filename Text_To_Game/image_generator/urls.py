# image_generator/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('generate-images/', views.generate_images_view, name='generate_images'),
]
