from django.db import models
from django.urls import reverse
from django.db.models.signals import post_delete
from django.dispatch import receiver

# Success Message: 3rd Tier Model 
class PeriodDetail(models.Model):
    count = models.IntegerField()
    source_id = models.CharField(max_length=200)

# Success Message: 2nd Tier Model 
class Period(models.Model):
    short_url_clicks = models.IntegerField()
    long_url_clicks = models.IntegerField()
    referrer = models.ManyToManyField(
        PeriodDetail,
        related_name='referrers',
        related_query_name='referrer'
        )
    country = models.ManyToManyField(
        PeriodDetail,
        related_name='countries',
        related_query_name='country'
        )
    browser = models.ManyToManyField(
        PeriodDetail,
        related_name='browsers',
        related_query_name='browser'
        )
    platform = models.ManyToManyField(
        PeriodDetail,
        related_name='platforms',
        related_query_name='platform'
        )

# Success Message: 1st Tier 
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

# Error Message: Tier 2 
class ErrorDetail(models.Model):
    domain = models.CharField(max_length=200)
    required = models.CharField(max_length=200)
    message = models.CharField(max_length=200)
    locationType = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

# Error Message: Tier 1
class Error(models.Model):
    error = models.OneToOneField(
        ErrorDetail,
        on_delete=models.CASCADE,
        )
    code = models.IntegerField()
    message = models.CharField(max_length=200)

