from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import redirect
from rest_framework import status
from .models import Url
from .serializers import OutputUrlSerializer, InputUrlSerializer
from .task import shorten_url_task

@api_view(["GET"])
def get_urls(request):
    """
    View for getting all the urls

    Output:
    [
        {
            "id": 1,
            "original_url": "https://www.example.com",
            "shortened_url": "f5f034"
        },
        {
            "id": 2,
            "original_url": "https://www.example2.com",
            "shortened_url": "f523a8"
        }
    ]
    """
    urls = Url.objects.all()
    return Response(
        OutputUrlSerializer(urls, many=True).data,
        status=status.HTTP_200_OK
    )

@api_view(["DELETE"])
def delete_url(request, id: int):
    """
    View for deleting the url

    Input:
        id: int

    Output:
    {
        "message": "The url has been deleted."
    }
    """
    url = Url.objects.filter(id=id).first()
    if url:
        url.delete()
        return Response(
            {"message": "The url has been deleted."},
            status=status.HTTP_200_OK
        )
    return Response(
        {"message": "The url does not exist."},
        status=status.HTTP_404_NOT_FOUND
    )

@api_view(["POST"])
def shorten_url(request):
    """
    View for shortening the url

    Input:
    {
        "original_url": "https://www.example.com"
    }

    Output:
    {
        "id": 1,
    }
    """
    serializer = InputUrlSerializer(data=request.data)
    if serializer.is_valid():
        original_url = serializer.validated_data["original_url"]
        # Check if the url is already shortened
        url = Url.objects.filter(original_url=original_url).first()
        if url:
            # If the url is already shortened, return the shortened url
            return Response(
                {"id": url.id},
                status=status.HTTP_200_OK
            )
        else: 
            # If the url is not shortened, create a new shortened url
            url = Url.objects.create(original_url=original_url)
            shorten_url_task.delay(url.id)
            return Response(
                {"id": url.id},
                status=status.HTTP_201_CREATED
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def redirect_view(request, short_url: str):
    """
    View for redirecting the shortened url to the original url

    Input:
        short_url: str
    """
    url = Url.objects.filter(short_url=short_url).first()
    if url:
        return redirect(url.original_url)
    return Response(
        {"message": "The url does not exist."},
        status=status.HTTP_404_NOT_FOUND
    )