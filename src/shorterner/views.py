from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.conf import settings
from django.urls import reverse
from django.views import View, generic
from .models import Urls

import requests
import json

from .forms import SubmitUrlForm

GOOGLE_URL_SHORTEN_API = 'AIzaSyC5OU6r75zEYM6EhewVg3rcBqOck7ZVBJg'

# def shorterner_index(request):
#     if request.method == "POST":
#         form = SubmitUrlForm(request.POST)
#         if form.is_valid():
#             input_url = form.cleaned_data['url']
#             short_url = google_url_shorten(input_url)

#             print(input_url)
#             print(short_url)

#             new_url = Urls.create(short_url, input_url)
#             new_url.save()

#             return HttpResponseRedirect('shorterner/list.html')
#     else:
#         form = SubmitUrl()
#     return render(request, 'shorterner/request.html', {'form': form})

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
            short_url = google_url_shorten(input_url)

            print(input_url)
            print(short_url)

            new_url = Urls.create(short_url, input_url)
            new_url.save()

            return render(request, '/shorterner/request/', {'id': ''})
        return render(request, self.template_name, {'form': form})


class IndexView(generic.ListView):
    template_name = 'shorterner/list.html'
    context_object_name = 'url_list'

    def get_queryset(self):
        return Urls.objects.all()



def google_url_shorten(url):
   req_url = 'https://www.googleapis.com/urlshortener/v1/url?key=' + GOOGLE_URL_SHORTEN_API
   payload = {'longUrl': url}
   headers = {'content-type': 'application/json'}
   r = requests.post(req_url, data=json.dumps(payload), headers=headers)
   resp = json.loads(r.text)
   return resp['id']