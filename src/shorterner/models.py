from django.db import models

class Urls(models.Model):
    short_url = models.CharField(max_length=200)
    input_url = models.CharField(max_length=200)
    analytics = models.OneToOneField(Analytics, on_delete=models.CASCADE, primary_key=True)),

    @classmethod
    def create(cls, short_url, input_url):
        urls = cls(
            short_url=short_url, 
            input_url=input_url,
            )
        return urls

    def __str__(self):
        return self.short_url

class Analytics(model.Model):
    status = models.CharField(max_length=10)
    created = models.DateTimeField()
    short_url_clicks = models.IntegerField()
    long_url_clicks = models.IntegerField()
 
class Referrers(model.Model):
    analytics_detail = models.ForeignKey(Analytics, on_delete=models.CASCADE)
    count = models.IntegerField()
    id = models.CharField(max_length=200)

class Countries(model.Model):
    analytics_detail = models.ForeignKey(Analytics, on_delete=models.CASCADE)
    count = models.IntegerField()
    id = models.CharField(max_length=200)

class Browsers(model.Model):
    analytics_detail = models.ForeignKey(Analytics, on_delete=models.CASCADE)
    count = models.IntegerField()
    id = models.CharField(max_length=200)

class Platforms(model.Model):
    analytics_detail = models.ForeignKey(Analytics, on_delete=models.CASCADE)
    count = models.IntegerField()
    id = models.CharField(max_length=200)

class Month(model.Model):
    analytics_detail = models.ForeignKey(Analytics, on_delete=models.CASCADE)
    count = models.IntegerField()
    id = models.CharField(max_length=200)

class Week(model.Model):
    analytics_detail = models.ForeignKey(Analytics, on_delete=models.CASCADE)
    count = models.IntegerField()
    id = models.CharField(max_length=200)

class Day(model.Model):
    analytics_detail = models.ForeignKey(Analytics, on_delete=models.CASCADE)
    count = models.IntegerField()
    id = models.CharField(max_length=200)

class TwoHours(model.Model):
    analytics_detail = models.ForeignKey(Analytics, on_delete=models.CASCADE)
    count = models.IntegerField()
    id = models.CharField(max_length=200)