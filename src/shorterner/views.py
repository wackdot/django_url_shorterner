from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings
from django.urls import reverse
from django.views import View, generic
from django.core import serializers
from .models import ErrorDetails, Error, Referrers, Countries, Browsers, Platforms, AllTime, Month, Week, Day, TwoHours
from django.core import serializers

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
                    if keys_exists(output_expand, 'analytics', 'allTime', 'referrers'):
                        allTime = output_expand.get('analytics').get('allTime').get('referrers')
                        referrer_list = []
                        for item in allTime:
                            # new_ref = Referrers.objects.create(
                            #     count = item.get('count'),
                            #     ref_id = item.get('id')
                            #     )
                            # referrer_list.append(new_ref)
                            new_ref = Referrers(
                                count = item.get('count'),
                                ref_id = item.get('id')
                                )
                            referrer_list.append(new_ref)

                        for item in referrer_list:
                            print(item)

                        # print(allTime[0].get('id'))
                        # print(allTime[0].get('count'))
                        # print(allTime[1].get('id'))
                        # print(allTime[1].get('count'))

                        # new_url.save()

                    # Unsuccessful tiny url creation
                  
                        # print(output.get('error', {}))

                        # errordetails = ErrorDetails.objects.create(
                        #     output.get('error', {}).get('errors', {}).get('domain', {}),
                        #     output.get('error')('errors')('required'),
                        #     output.get('error')('errors')('message'),
                        #     output('error')('errors')('locationType'),
                        #     output('error')('errors')('location')
                        # )
                        # error = Error.objects.create(
                        #     errordetails,
                        #     output.get('code'),
                        #     output.get('message')
                        # )
                        # error.save()
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