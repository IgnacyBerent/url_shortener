from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Url
from .serializers import OutputUrlSerializer, InputUrlSerializer
from .task import shorten_url_task

@swagger_auto_schema(
    method='get',
    operation_description="View for getting all the urls",
    responses={
        200: openapi.Response(
            description="A list of URLs",
            examples={
                "application/json": [
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
            }
        )
    }
)
@api_view(["GET"])
def get_urls(request):
    urls = Url.objects.all()
    return Response(
        OutputUrlSerializer(urls, many=True).data,
        status=status.HTTP_200_OK
    )

@swagger_auto_schema(
    method='delete',
    operation_description="View for deleting the url",
    responses={
        200: openapi.Response(
            description="The url has been deleted.",
            examples={
                "application/json": {
                    "message": "The url has been deleted."
                }
            }
        ),
        404: openapi.Response(
            description="The url does not exist.",
            examples={
                "application/json": {
                    "message": "The url does not exist."
                }
            }
        )
    }
)
@api_view(["DELETE"])
def delete_url(request, id: int):
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

@swagger_auto_schema(
    method='post',
    operation_description="View for shortening the url",
    request_body=InputUrlSerializer,
    responses={
        201: openapi.Response(
            description="The url has been shortened.",
            examples={
                "application/json": {
                    "id": 1
                }
            }
        ),
        200: openapi.Response(
            description="The url is already shortened.",
            examples={
                "application/json": {
                    "id": 1
                }
            }
        ),
        400: "Bad Request"
    }
)
@api_view(["POST"])
def shorten_url(request):
    serializer = InputUrlSerializer(data=request.data)
    if serializer.is_valid():
        original_url = serializer.validated_data["original_url"]
        url = Url.objects.filter(original_url=original_url).first()
        if url:
            return Response(
                {"id": url.id},
                status=status.HTTP_200_OK
            )
        else:
            url = Url.objects.create(original_url=original_url)
            shorten_url_task.delay(url.id)
            return Response(
                {"id": url.id},
                status=status.HTTP_201_CREATED
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='get',
    operation_description="View for redirecting the shortened url to the original url",
    responses={
        302: openapi.Response(
            description="Redirect to the original URL",
            examples={
                "application/json": {
                    "message": "Redirecting to the original URL."
                }
            }
        ),
        404: openapi.Response(
            description="The url does not exist.",
            examples={
                "application/json": {
                    "message": "The url does not exist."
                }
            }
        )
    }
)
@api_view(["GET"])
def redirect_view(request, short_url: str):
    url = Url.objects.filter(short_url=short_url).first()
    if url:
        return redirect(url.original_url)
    return Response(
        {"message": "The url does not exist."},
        status=status.HTTP_404_NOT_FOUND
    )

@swagger_auto_schema(
    method='get',
    operation_description="View for getting the shortened url",
    responses={
        200: openapi.Response(
            description="Shortened URL",
            examples={
                "application/json": {
                    "shortened_url": "f5f034"
                }
            }
        ),
        404: openapi.Response(
            description="The url does not exist.",
            examples={
                "application/json": {
                    "message": "The url does not exist."
                }
            }
        )
    }
)
@api_view(["GET"])
def get_shorten_url(request, id: int):
    url = Url.objects.filter(id=id).first()
    if url:
        return Response(
            {"shortened_url": url.short_url},
            status=status.HTTP_200_OK
        )
    return Response(
        {"message": "The url does not exist."},
        status=status.HTTP_404_NOT_FOUND
    )

@swagger_auto_schema(
    method='get',
    operation_description="View for health check",
    responses={
        200: openapi.Response(
            description="The server is running.",
            examples={
                "application/json": {
                    "message": "The server is running."
                }
            }
        )
    }
)
@api_view(["GET"])
def health_check(request):
    return Response(
        {"message": "The server is running."},
        status=status.HTTP_200_OK
    )