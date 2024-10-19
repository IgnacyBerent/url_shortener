from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def list_urls(request):
    return render(request, 'list_urls.html')