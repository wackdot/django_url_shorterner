from django.db import models

class Urls(models.Model):
    short_url = models.CharField(max_length=200)
    input_url = models.CharField(max_length=200)

    @classmethod
    def create(cls, short_url, input_url):
        urls = cls(
            short_url=short_url, 
            input_url=input_url
            )
        return urls

