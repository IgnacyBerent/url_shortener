from django.urls import path
from .views import shorten_url, get_urls, delete_url, redirect_view, health_check, get_shorten_url

urlpatterns = [
    path("get_urls/", get_urls, name='get_urls'),
    path("shorten_url/", shorten_url, name='shorten_url'),
    path("delete_url/<int:id>/", delete_url, name='delete_url'),
    path("<str:short_url>/", redirect_view, name='redirect_view'),
    path("get_shorten_url/<int:id>/", get_shorten_url, name='get_shorten_url'),
    path("health_check/", health_check, name='health_check'),
]