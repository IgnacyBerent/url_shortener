from django.urls import path
from .views import shorten_url, get_urls, delete_url, redirect

urlpatterns = [
    path("get_urls/", get_urls),
    path("shorten_url/", shorten_url),
    path("delete_url/<int:id>/", delete_url),
]