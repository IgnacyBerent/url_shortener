from django.db import models

"""
Model for stroring url data
"""
class Url(models.Model):
    original_url = models.URLField(max_length=200)
    short_url = models.URLField(max_length=200)

    def __str__(self):
        return self.original_url