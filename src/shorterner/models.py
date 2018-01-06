from django.db import models
from django.urls import reverse
from django.db.models.signals import post_delete
from django.dispatch import receiver

# Success Message: Tier 3 
class PeriodDetail(models.Model):
    count = models.IntegerField()
    source_id = models.CharField(max_length=200)

# Error Message: Tier 3
class ErrorDetail(models.Model):
    domain = models.CharField(max_length=200)
    reason = models.CharField(max_length=200)
    message = models.CharField(max_length=200)
    locationType = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

# Success Message: Tier 2 
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

# Error Message: Tier 2
class Error(models.Model):
    error = models.OneToOneField(
        ErrorDetail,
        on_delete=models.CASCADE,
        )
    code = models.IntegerField()
    message = models.CharField(max_length=200)


# Success Message: Tier 1 
# Charfields should only be set to blank (Empty string), null is not required
# Datetime set blank(For admin), null(db storage)
class Url(models.Model):
    short_url = models.CharField(
        max_length=200,
        blank=True
        )
    input_url = models.CharField(max_length=200)
    status = models.CharField(
        max_length=10,
        blank=True
        )
    created = models.DateTimeField(
        blank=True,
        null=True
        )
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
    errormessage = models.OneToOneField(
        Error,
        on_delete=models.CASCADE,
        null=True,
        related_name='errormessages',
        related_query_name='errormessage'
        )
    
    def __str__(self):
        return self.input_url

    @property
    def title(self):
        return self.input_url


