from __future__ import absolute_import, unicode_literals

from celery import shared_task
from .models import Url
import uuid

@shared_task
def shorten_url_task(url_id: int):
    """
    Task for shortening the url
    """
    url = Url.objects.filter(id=url_id).first()
    url.short_url = str(uuid.uuid4())[:6]
    url.save()
    