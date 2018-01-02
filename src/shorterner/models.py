from django.db import models
from django.urls import reverse

class Urls(models.Model):
    short_url = models.CharField(max_length=200)
    input_url = models.CharField(max_length=200)
    status = models.CharField(max_length=10)
    created = models.DateTimeField()

    @classmethod
    def create(cls, short_url, input_url, Analytics):
        urls = cls(
            short_url=short_url, 
            input_url=input_url,
            )
        return urls

    def __str__(self):
        return self.short_url

    def get_absolute_url(self):
        return reverse('shorterner:details', kwargs={'slug': self.short_url})
    
    @property
    def title(self):
        return self.short_url

# 2nd Tier Models
class AllTime(models.Model):
    url_id = models.ForeignKey(Urls, on_delete=models.CASCADE)
    short_url_clicks = models.IntegerField()
    long_url_clicks = models.IntegerField()
    referrers = models.ManyToManyField(Referrers)
    countries = models.ManyToManyField(Countries)
    browsers = models.ManyToManyField(Browsers)
    platforms = models.ManyToManyField(platforms)

class Month(models.Model):
    url_id = models.ForeignKey(Urls, on_delete=models.CASCADE)
    short_url_clicks = models.IntegerField()
    long_url_clicks = models.IntegerField()
    referrers = models.ManyToManyField(Referrers)
    countries = models.ManyToManyField(Countries)
    browsers = models.ManyToManyField(Browsers)
    platforms = models.ManyToManyField(platforms)


class Week(models.Model):
    url_id = models.ForeignKey(Urls, on_delete=models.CASCADE)
    short_url_clicks = models.IntegerField()
    long_url_clicks = models.IntegerField()
    referrers = models.ManyToManyField(Referrers)
    countries = models.ManyToManyField(Countries)
    browsers = models.ManyToManyField(Browsers)
    platforms = models.ManyToManyField(platforms)

class Day(models.Model):
    url_id = models.ForeignKey(Urls, on_delete=models.CASCADE)
    short_url_clicks = models.IntegerField()
    long_url_clicks = models.IntegerField()
    referrers = models.ManyToManyField(Referrers)
    countries = models.ManyToManyField(Countries)
    browsers = models.ManyToManyField(Browsers)
    platforms = models.ManyToManyField(platforms)

class TwoHours(models.Model):
    url_id = models.ForeignKey(Urls, on_delete=models.CASCADE)
    short_url_clicks = models.IntegerField()
    long_url_clicks = models.IntegerField()
    referrers = models.ManyToManyField(Referrers)
    countries = models.ManyToManyField(Countries)
    browsers = models.ManyToManyField(Browsers)
    platforms = models.ManyToManyField(platforms)

# 3rd Tier Models
class Referrers(models.Model):
    count = models.IntegerField()
    ref_id = models.CharField(max_length=200)

class Countries(models.Model):
    count = models.IntegerField()
    country_id = models.CharField(max_length=200)

class Browsers(models.Model):
    count = models.IntegerField()
    browser_id = models.CharField(max_length=200)

class Platforms(models.Model):
    count = models.IntegerField()
    platform_id = models.CharField(max_length=200)