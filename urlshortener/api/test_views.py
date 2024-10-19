from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Url

class UrlShortenerTests(APITestCase):

    def setUp(self):
        self.url1 = Url.objects.create(original_url="https://www.example.com", short_url="f5f034")
        self.url2 = Url.objects.create(original_url="https://www.example2.com", short_url="f523a8")

    def test_get_urls(self):
        response = self.client.get(reverse('get_urls'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_delete_url(self):
        response = self.client.delete(reverse('delete_url', args=[self.url1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "The url has been deleted.")
        self.assertFalse(Url.objects.filter(id=self.url1.id).exists())

    def test_shorten_url(self):
        data = {"original_url": "https://www.example3.com"}
        response = self.client.post(reverse('shorten_url'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['original_url'], "https://www.example3.com")
        self.assertTrue(Url.objects.filter(original_url="https://www.example3.com").exists())

    def test_redirect_view(self):
        response = self.client.get(reverse('redirect_view', args=[self.url1.short_url]))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, self.url1.original_url)