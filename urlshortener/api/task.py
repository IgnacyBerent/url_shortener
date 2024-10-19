from __future__ import absolute_import, unicode_literals

from celery import shared_task
from .models import Url
import uuid
import time

@shared_task
def shorten_url_task(url_id: int):
    """
    Task for shortening the url
    """
    # Simulating a delay
    time.sleep(5)
    url = Url.objects.filter(id=url_id).first()
    if url:
        url.short_url = str(uuid.uuid4())[:6]
        url.save()
    else:
        # Handle the case where the URL is not found
        print(f"Url with id {url_id} not found.")