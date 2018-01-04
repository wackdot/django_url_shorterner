from django.contrib import admin
from .models import Error, ErrorDetails, Period, PeriodDetails, Urls

shorterner_models = [Error, ErrorDetails, Period, PeriodDetails, Urls]
admin.site.register(shorterner_models)