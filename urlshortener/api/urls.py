from django.urls import path
from .views import shorten_url, get_urls

urlpatterns = [
    path("get_urls/", get_urls),
    path("shorten_url/", shorten_url),
]