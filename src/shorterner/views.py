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
                    # Retrieving and storing values
                    # Tier 3
                    # All Time
                    alltime_list = []
                    alltime_list.append(create_period_detail(output_expand, 'analytics', 'allTime', 'referrers'))
                    alltime_list.append(create_period_detail(output_expand, 'analytics', 'allTime', 'countries'))
                    alltime_list.append(create_period_detail(output_expand, 'analytics', 'allTime', 'browsers'))
                    alltime_list.append(create_period_detail(output_expand, 'analytics', 'allTime', 'platforms'))
                    
                    # # # Month
                    # month_list = [
                    #     month_referrers = create_period_detail(output_expand, 'analytics', 'month', 'referrers'),
                    #     month_countries = create_period_detail(output_expand, 'analytics', 'month', 'countries'),
                    #     month_browsers = create_period_detail(output_expand, 'analytics', 'month', 'browsers'),
                    #     month_platforms = create_period_detail(output_expand, 'analytics', 'month', 'platforms')
                    # ]

                    # # # Week
                    # week_list = [
                    #     week_referrers = create_period_detail(output_expand, 'analytics', 'week', 'referrers'),
                    #     week_countries = create_period_detail(output_expand, 'analytics', 'week', 'countries'),
                    #     week_browsers = create_period_detail(output_expand, 'analytics', 'week', 'browsers'),
                    #     week_platforms = create_period_detail(output_expand, 'analytics', 'week', 'platforms')
                    # ]
                    
                    # # # Day
                    # day_list = [
                    #     day_referrers = create_period_detail(output_expand, 'analytics', 'day', 'referrers'),
                    #     day_countries = create_period_detail(output_expand, 'analytics', 'day', 'countries'),
                    #     day_browsers = create_period_detail(output_expand, 'analytics', 'day', 'browsers'),
                    #     day_platforms = create_period_detail(output_expand, 'analytics', 'day', 'platforms')
                    # ]

                    # # # twoHours
                    # twoHours_list = [
                    #     twoHours_referrers = create_period_detail(output_expand, 'analytics', 'twoHours', 'referrers'),
                    #     twoHours_countries = create_period_detail(output_expand, 'analytics', 'twoHours', 'countries'),
                    #     twoHours_browsers = create_period_detail(output_expand, 'analytics', 'twoHours', 'browsers'),
                    #     twoHours_platforms = create_period_detail(output_expand, 'analytics', 'twoHours', 'platforms')
                    # ]

                    # Tier 2
                    test = create_period(output_expand, alltime_list, 'analytics', 'allTime', 'shortUrlClicks', 'longUrlClicks')


                    # alltime = Period(
                    #     short_url_clicks = int(output_expand.get('analytics').get('allTime').get('shortUrlClicks')),
                    #     long_url_clicks = int(output_expand.get('analytics').get('allTime').get('longUrlClicks'))                       
                    # )
                    # alltime.save()
                    # for item in alltime_referrers:
                    #     alltime.referrers.add(item)
                    # for item in alltime_countries:
                    #     alltime.countries.add(item)
                    # for item in alltime_browsers:
                    #     alltime.browsers.add(item)
                    # for item in alltime_platforms:
                    #     alltime.platforms.add(item)
                    # alltime.save()

                    # month = Period(
                    #     short_url_clicks = int(output_expand.get('analytics').get('month').get('shortUrlClicks')),
                    #     long_url_clicks = int(output_expand.get('analytics').get('month').get('longUrlClicks')),
                    # )
                    # month.save()
                    # for item in month_referrers:
                    #     month.referrers.add(item)
                    # for item in month_countries:
                    #     month.countries.add(item)
                    # for item in month_browsers:
                    #     month.browsers.add(item)
                    # for item in month_platforms:
                    #     month.platforms.add(item)
                    # month.save()

                    # week = Period(
                    #     short_url_clicks = output_expand.get('analytics').get('week').get('shortUrlClicks'),
                    #     long_url_clicks = output_expand.get('analytics').get('week').get('longUrlClicks'),
                    #     referrers = week_referrers,
                    #     countries = week_countries,
                    #     browsers = week_browsers,
                    #     platforms = week_platforms
                    # )
                    # print(week)

                    # day = Period(
                    #     short_url_clicks = output_expand.get('analytics').get('day').get('shortUrlClicks'),
                    #     long_url_clicks = output_expand.get('analytics').get('day').get('longUrlClicks'),
                    #     referrers = day_referrers,
                    #     countries = day_countries,
                    #     browsers = day_browsers,
                    #     platforms = day_platforms
                    # )
                    # print(day)

                    # twoHours = Period(
                    #     short_url_clicks = output_expand.get('analytics').get('twoHours').get('shortUrlClicks'),
                    #     long_url_clicks = output_expand.get('analytics').get('twoHours').get('longUrlClicks'),
                    #     referrers = twoHours_referrers,
                    #     countries = twoHours_countries,
                    #     browsers = twoHours_browsers,
                    #     platforms = twoHours_platforms
                    # )
                    # print(twoHours)

                    # # Create Url
                    # new_url = Urls(
                    #     short_url = output_expand.get('id'),
                    #     input_url = output_expand.get('longUrl'),
                    #     status = output_expand.get('status'),
                    #     created = output_expand.get('created'),
                    #     allTime = alltime,
                    #     month = month,
                    #     week = week,
                    #     day = day,
                    #     twohours = twoHours                        
                    # )

                    # for attr, value in new_url.__dict__.iteritems():
                    #     print(attr, value)

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

def create_period_detail(obj_dict, *keys):
    return_list = []
    if keys_exists(obj_dict, *keys):
        obj_list = obj_dict.get(keys[0]).get(keys[1]).get(keys[2])
        for item in obj_list:
            new_item = PeriodDetails(
                count = int(item.get('count')),
                source_id = item.get('id')
                )
            new_item.save() #Requires the object to be saved before it can be added as part of another object
            return_list.append(new_item)
    return return_list


def create_period(obj_dict, obj_list, *keys):
    if keys_exists(obj_dict, *keys):
        output = Period(
            short_url_clicks = int(obj_dict.get(keys[0]).get(keys[1]).get(keys[2])),
            long_url_clicks = int(obj_dict.get(keys[0]).get(keys[1]).get(keys[3]))
        )
        output.save()
        for index, list in enumerate(obj_list):
            for PeriodDetails in list:
                print(index)


