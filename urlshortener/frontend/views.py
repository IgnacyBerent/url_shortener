from django.shortcuts import render

def index(request):
    """
    View function for the home page of the site. Its simple interface allows users to shorten URLs.
    """
    return render(request, 'index.html')

def list_urls(request):
    """
    View function for the page that lists all shortened URLs.
    """
    return render(request, 'list_urls.html')