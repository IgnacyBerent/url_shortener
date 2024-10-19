from django.urls import path
from .views import index, list_urls

urlpatterns = [
    path('', index, name='index'),
    path('list_urls/', list_urls, name='list_urls'),
]