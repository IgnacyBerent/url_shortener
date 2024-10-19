from django.urls import path
from .views import shorten_url, get_urls, delete_url, redirect_view, health_check, get_shorten_url

urlpatterns = [
    path("get_urls/", get_urls),
    path("shorten_url/", shorten_url),
    path("delete_url/<int:id>/", delete_url),
    path("<str:short_url>/", redirect_view),
    path("get_shorten_url/<int:id>/", get_shorten_url),
    path("health_check/", health_check),
]