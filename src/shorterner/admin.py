from django.contrib import admin
from .models import Error, ErrorDetail, Period, PeriodDetail, Url

shorterner_models = [Error, ErrorDetail, Period, PeriodDetail, Url]
admin.site.register(shorterner_models)