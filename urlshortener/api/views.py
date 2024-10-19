from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Url
from .serializers import OutputUrlSerializer, InputUrlSerializer
from .task import shorten_url_task

@api_view(["GET"])
def get_urls(request):
    """
    View for getting all the urls
    """
    urls = Url.objects.all()
    return Response(
        OutputUrlSerializer(urls, many=True).data,
        status=status.HTTP_200_OK
    )

@api_view(["POST"])
def shorten_url(request):
    """
    View for shortening the url
    """
    serializer = InputUrlSerializer(data=request.data)
    if serializer.is_valid():
        original_url = serializer.validated_data["original_url"]
        # Check if the url is already shortened
        url = Url.objects.filter(original_url=original_url).first()
        if url:
            # If the url is already shortened, return the shortened url
            return Response(
                OutputUrlSerializer(url).data,
                status=status.HTTP_200_OK
            )
        else: 
            url = Url.objects.create(original_url=original_url)
            shorten_url_task.delay(url.id)
            # Return message that the url is being shortened
            return Response(
                {"message": "The url is being shortened. Please wait."},
                status=status.HTTP_201_CREATED
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)