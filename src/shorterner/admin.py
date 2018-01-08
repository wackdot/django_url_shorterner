from django.contrib import admin
from .models import Error, Period, PeriodDetail, Url

shorterner_models = [Error, Period, PeriodDetail, Url]
admin.site.register(shorterner_models)