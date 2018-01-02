from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings
from django.urls import reverse
from django.views import View, generic
from django.core import serializers
from . import models

import requests
import json

from .forms import SubmitUrlForm

API_KEY = 'AIzaSyC5OU6r75zEYM6EhewVg3rcBqOck7ZVBJg'

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
            output = google_url_full(input_url)
            print(output)

            #Coverting JSON to model
            json_data = json.dumps(output)
            for deserialized_obj in serializers.deserialize("json", json_data):
                deserialized_obj.save()

            # new_url = Urls.create(
            #     output['id'], 
            #     output['longUrl'], 
            #     output['status'],
            #     output['created'],
            #     AllTime.create(
            #         output['analytics'].['allTime'].['shortUrlClicks'],
            #         output
            #     )
            # )
            # new_url.save()
            return HttpResponseRedirect(reverse('shorterner:list')) # change to error page, invalid url
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
   return resp['id']

def google_url_full(url):
    req_url = 'https://www.googleapis.com/urlshortener/v1/url?/fbsS&projection=FULL' # Remove the parameters in the url, only retain the required string
    payload = {'key': API_KEY, 'shortUrl': url} # Using key value pairs to populate the url
    r = requests.get(req_url, params=payload)
    resp = json.loads(r.text)
    return resp

