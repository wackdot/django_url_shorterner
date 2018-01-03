from django.db import models
from django.urls import reverse

# 3rd Tier Models
# Success 
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

# 2nd Tier Models
# Success
class AllTime(models.Model):
    short_url_clicks = models.IntegerField()
    long_url_clicks = models.IntegerField()
    referrers = models.ManyToManyField(Referrers)
    countries = models.ManyToManyField(Countries)
    browsers = models.ManyToManyField(Browsers)
    platforms = models.ManyToManyField(Platforms)

class Month(models.Model):
    short_url_clicks = models.IntegerField()
    long_url_clicks = models.IntegerField()
    referrers = models.ManyToManyField(Referrers)
    countries = models.ManyToManyField(Countries)
    browsers = models.ManyToManyField(Browsers)
    platforms = models.ManyToManyField(Platforms)


class Week(models.Model):
    short_url_clicks = models.IntegerField()
    long_url_clicks = models.IntegerField()
    referrers = models.ManyToManyField(Referrers)
    countries = models.ManyToManyField(Countries)
    browsers = models.ManyToManyField(Browsers)
    platforms = models.ManyToManyField(Platforms)

class Day(models.Model):
    short_url_clicks = models.IntegerField()
    long_url_clicks = models.IntegerField()
    referrers = models.ManyToManyField(Referrers)
    countries = models.ManyToManyField(Countries)
    browsers = models.ManyToManyField(Browsers)
    platforms = models.ManyToManyField(Platforms)

class TwoHours(models.Model):
    short_url_clicks = models.IntegerField()
    long_url_clicks = models.IntegerField()
    referrers = models.ManyToManyField(Referrers)
    countries = models.ManyToManyField(Countries)
    browsers = models.ManyToManyField(Browsers)
    platforms = models.ManyToManyField(Platforms)

# Error Message
class ErrorDetails(models.Model):
    domain = models.CharField(max_length=200)
    required = models.CharField(max_length=200)
    message = models.CharField(max_length=200)
    locationType = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

# 1st Tier Models
class Urls(models.Model):
    short_url = models.CharField(max_length=200)
    input_url = models.CharField(max_length=200)
    status = models.CharField(max_length=10)
    created = models.DateTimeField()
    alltime = models.OneToOneField(
        AllTime,
        on_delete=models.CASCADE,
        primary_key=True,
        )
    month = models.OneToOneField(
        Month,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    week = models.OneToOneField(
        Week,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    day = models.OneToOneField(
        Day,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    twohours = models.OneToOneField(
        TwoHours,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return self.short_url

    def get_absolute_url(self):
        return reverse('shorterner:details', kwargs={'slug': self.short_url})
    
    @property
    def title(self):
        return self.short_url

class Error(models.Model):
    error = models.OneToOneField(
        ErrorDetails,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    code = models.IntegerField()
    message = models.CharField(max_length=200)

