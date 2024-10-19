from __future__ import absolute_import, unicode_literals

from celery import shared_task
from .models import Url
import uuid

@shared_task
def shorten_url_task(url_id):
    """
    Task for shortening the url
    """
    url = Url.objects.get(id=url_id)
    url.short_url = uuid.uuid4().hex[:6]
    url.save()
    