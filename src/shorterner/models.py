from django.db import models
from django.urls import reverse
from django.db.models.signals import post_delete
from django.dispatch import receiver

# 3rd Tier Models
# Success 
class PeriodDetail(models.Model):
    count = models.IntegerField()
    source_id = models.CharField(max_length=200)

# 2nd Tier Models
# Success
class Period(models.Model):
    short_url_clicks = models.IntegerField()
    long_url_clicks = models.IntegerField()
    referrer = models.ForeignKey(
        PeriodDetail, 
        related_name='referrers', 
        related_query_name='referrer',
        on_delete=models.CASCADE,
        null=True
        )
    country = models.ForeignKey(
        PeriodDetail, 
        related_name='countries', 
        related_query_name='country',
        on_delete=models.CASCADE,
        null=True    
        )
    browser = models.ForeignKey(
        PeriodDetail, 
        related_name='browsers', 
        related_query_name='browser',
        on_delete=models.CASCADE,
        null=True
        )
    platform = models.ForeignKey(
        PeriodDetail, 
        related_name='platforms', 
        related_query_name='platform',
        on_delete=models.CASCADE,
        null=True
        )

# Error Message
class ErrorDetail(models.Model):
    domain = models.CharField(max_length=200)
    required = models.CharField(max_length=200)
    message = models.CharField(max_length=200)
    locationType = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

# 1st Tier Models
class Url(models.Model):
    short_url = models.CharField(max_length=200)
    input_url = models.CharField(max_length=200)
    status = models.CharField(max_length=10)
    created = models.DateTimeField()
    alltime = models.OneToOneField(
        Period,
        on_delete=models.CASCADE,
        null=True,
        related_name='alltimes', 
        related_query_name='alltime',
        )
    month = models.OneToOneField(
        Period,
        on_delete=models.CASCADE,
        null=True,
        related_name='months', 
        related_query_name='month',
        )
    week = models.OneToOneField(
        Period,
        on_delete=models.CASCADE,
        null=True,
        related_name='weeks', 
        related_query_name='week',
        )
    day = models.OneToOneField(
        Period,
        on_delete=models.CASCADE,
        null=True,
        related_name='days', 
        related_query_name='day',
        )
    twohour = models.OneToOneField(
        Period,
        on_delete=models.CASCADE,
        null=True,
        related_name='twohours', 
        related_query_name='twohour',
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
        ErrorDetail,
        on_delete=models.CASCADE,
    )
    code = models.IntegerField()
    message = models.CharField(max_length=200)
