from django.db import models
from django.urls import reverse

# 3rd Tier Models
# Success 
class PeriodDetails(models.Model):
    count = models.IntegerField()
    source_id = models.CharField(max_length=200)

# 2nd Tier Models
# Success
class Period(models.Model):
    short_url_clicks = models.IntegerField()
    long_url_clicks = models.IntegerField()
    referrers = models.ManyToManyField(
        PeriodDetails, 
        related_name='%(class)s_referrers', 
        related_query_name="%(app_label)s_%(class)ss",
        blank=True)
    countries = models.ManyToManyField(
        PeriodDetails, 
        related_name='%(class)s_countries', 
        related_query_name="%(app_label)s_%(class)ss",
        blank=True)
    browsers = models.ManyToManyField(
        PeriodDetails, 
        related_name='%(class)s_browsers',
        related_query_name="%(app_label)s_%(class)ss",
        blank=True)
    platforms = models.ManyToManyField(
        PeriodDetails, 
        related_name='%(class)s_platforms', 
        related_query_name="%(app_label)s_%(class)ss",
        blank=True)

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
        Period,
        on_delete=models.CASCADE,
        related_name='%(class)s_alltime',
        related_query_name="%(app_label)s_%(class)ss",
        )
    month = models.OneToOneField(
        Period,
        on_delete=models.CASCADE,
        related_name='%(class)s_month',
        related_query_name="%(app_label)s_%(class)ss",
    )
    week = models.OneToOneField(
        Period,
        on_delete=models.CASCADE,
        related_name='%(class)s_week',
        related_query_name="%(app_label)s_%(class)ss",
    )
    day = models.OneToOneField(
        Period,
        on_delete=models.CASCADE,
        related_name='%(class)s_day',
        related_query_name="%(app_label)s_%(class)ss",
    )
    twohours = models.OneToOneField(
        Period,
        on_delete=models.CASCADE,
        related_name='%(class)s_twohours',
        related_query_name="%(app_label)s_%(class)ss",
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
    )
    code = models.IntegerField()
    message = models.CharField(max_length=200)

