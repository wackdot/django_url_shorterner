from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings
from django.urls import reverse
from django.views import View, generic
from django.core import serializers
from .models import ErrorDetails, Error, Period, PeriodDetails

import requests
import json

from .forms import SubmitUrlForm

API_KEY = 'AIzaSyCl52P8Tw1VoGD6EDw7dAZgmtalmVStQcs'

class RequestView(View):
    form_class = SubmitUrlForm
    initial = { 'url': ''}
    template_name = "shorterner/request.html"
    context_object_name = 'url'

    def form_valid(self, form):
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            input_url = form.cleaned_data['url']
            print("The input url is: %s" % input_url)

            # Create tiny url
            output_short = google_url_shorten(input_url)
            print("The response: %s" % output_short)

            # Verify response type (Successful url creation)
            if 'id' in output_short:
                short_url = output_short['id']
                print("Extracting the short url: %s" % short_url)

                # Successful tiny url creation, retrieve analytics data
                output_expand = google_url_expand(short_url)
                print(output_expand)
                
                # Successful analytics call
                if 'created' in output_expand:
                    # created_url_object(output_expand)

                    # Retrieving and storing values
                    # Tier 3
                    # All Time
                    alltime_referrers = created_url_object(output_expand, 'analytics', 'allTime', 'referrers')
                    alltime_countries = created_url_object(output_expand, 'analytics', 'allTime', 'countries')
                    alltime_browsers = created_url_object(output_expand, 'analytics', 'allTime', 'browsers')
                    alltime_platforms = created_url_object(output_expand, 'analytics', 'allTime', 'platforms')

                    # Month
                    month_referrers = created_url_object(output_expand, 'analytics', 'month', 'referrers')
                    month_countries = created_url_object(output_expand, 'analytics', 'month', 'countries')
                    month_browsers = created_url_object(output_expand, 'analytics', 'month', 'browsers')
                    month_platforms = created_url_object(output_expand, 'analytics', 'month', 'platforms')

                    # Week
                    week_referrers = created_url_object(output_expand, 'analytics', 'week', 'referrers')
                    week_countries = created_url_object(output_expand, 'analytics', 'week', 'countries')
                    week_browsers = created_url_object(output_expand, 'analytics', 'week', 'browsers')
                    week_platforms = created_url_object(output_expand, 'analytics', 'week', 'platforms')

                    # Day
                    day_referrers = created_url_object(output_expand, 'analytics', 'day', 'referrers')
                    day_countries = created_url_object(output_expand, 'analytics', 'day', 'countries')
                    day_browsers = created_url_object(output_expand, 'analytics', 'day', 'browsers')
                    day_platforms = created_url_object(output_expand, 'analytics', 'day', 'platforms')
                    
                    # twoHours
                    twoHours_referrers = created_url_object(output_expand, 'analytics', 'twoHours', 'referrers')
                    twoHours_countries = created_url_object(output_expand, 'analytics', 'twoHours', 'countries')
                    twoHours_browsers = created_url_object(output_expand, 'analytics', 'twoHours', 'browsers')
                    twoHours_platforms = created_url_object(output_expand, 'analytics', 'twoHours', 'platforms')

                    # Tier 2
                    alltime = Period(
                        short_url_clicks = output_expand.get('allTime').get('shortUrlClicks'),
                        long_url_clicks = output_expand.get('allTime').get('longUrlClicks'),
                        referrers = alltime_referrers,
                        countries = alltime_countries,
                        browsers = alltime_browsers,
                        platforms = alltime_platforms
                    )
                    print(alltime)
                    month = Period(
                        short_url_clicks = output_expand.get('month').get('shortUrlClicks'),
                        long_url_clicks = output_expand.get('month').get('longUrlClicks'),
                        referrers = month_referrers,
                        countries = month_countries,
                        browsers = month_browsers,
                        platforms = month_platforms
                    )
                    print(month)
                    week = Period(
                        short_url_clicks = output_expand.get('week').get('shortUrlClicks'),
                        long_url_clicks = output_expand.get('week').get('longUrlClicks'),
                        referrers = week_referrers,
                        countries = week_countries,
                        browsers = week_browsers,
                        platforms = week_platforms
                    )
                    print(week)
                    day = Period(
                        short_url_clicks = output_expand.get('day').get('shortUrlClicks'),
                        long_url_clicks = output_expand.get('day').get('longUrlClicks'),
                        referrers = day_referrers,
                        countries = day_countries,
                        browsers = day_browsers,
                        platforms = day_platforms
                    )
                    print(day)
                    twoHours = Period(
                        short_url_clicks = output_expand.get('twoHours').get('shortUrlClicks'),
                        long_url_clicks = output_expand.get('twoHours').get('longUrlClicks'),
                        referrers = twoHours_referrers,
                        countries = twoHours_countries,
                        browsers = twoHours_browsers,
                        platforms = twoHours_platforms
                    )
                    print(twoHours)

                    # Create Url
                    # new_url = Urls(
                    #     short_url = output_expand.get('id'),
                    #     input_url = output_expand.get('longUrl'),
                    #     status = output_expand.get('status'),
                    #     created = output_expand.get('created'),
                    #     allTime = 
                    # )

                    # new_url.save()


                    # Unsuccessful tiny url creation


            return HttpResponseRedirect(reverse('shorterner:request')) # change to error page, invalid url
        return render(request, self.template_name, {'form': form})

class IndexView(generic.ListView):
    template_name = 'shorterner/list.html'
    context_object_name = 'url_list'

    def get_queryset(self):
        return Urls.objects.all()

# class DetailView(generic.DetailView):
#     template_name = "shorterner/detail.html"
#     model = Analytics


def google_url_shorten(url):
   req_url = 'https://www.googleapis.com/urlshortener/v1/url?key=' + API_KEY
   payload = {'longUrl': url}
   headers = {'content-type': 'application/json'}
   r = requests.post(req_url, data=json.dumps(payload), headers=headers)
   resp = json.loads(r.text)
   return resp

# def google_url_full(url):
#     req_url = 'https://www.googleapis.com/urlshortener/v1/url?shortUrl=/fbsS&projection=FULL' # Remove the parameters in the url, only retain the required string
#     payload = {'key': API_KEY, 'shortUrl': url} # Using key value pairs to populate the url
#     r = requests.get(req_url, params=payload)
#     resp = json.loads(r.text)
#     return resp

def google_url_expand(url):
    req_url = 'https://www.googleapis.com/urlshortener/v1/url' 
    payload = {'key': API_KEY, 'shortUrl': url, 'projection': 'full'}
    r = requests.get(req_url, params=payload)
    resp = json.loads(r.text)
    return resp

def keys_exists(element, *keys):
    '''
    Check if *keys (nested) exists in `element` (dict).
    '''
    if type(element) is not dict:
        raise AttributeError('keys_exists() expects dict as first argument.')
    if len(keys) == 0:
        raise AttributeError('keys_exists() expects at least two arguments, one given.')

    _element = element
    for key in keys:
        try:
            _element = _element[key]
        except KeyError:
            return False
    return True

# Rename object to create_period_object
def created_url_object(obj_dict, *keys):
    return_list = []
    if keys_exists(obj_dict, keys):
        obj_list = obj_dict.get(keys[0]).get(keys[1]).get(keys[2])
        for item in obj_list:
            new_item = PeriodDetails(
                count = item.get('count'),
                source_id = item.get('id')
                )
            return_list.append(new_item)
            print(new_item)
    return return_list

