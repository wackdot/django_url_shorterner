from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings
from django.urls import reverse
from django.views import View, generic
from django.core import serializers

from .models import ErrorDetails, Error, Period, PeriodDetails, Urls
from .forms import SubmitUrlForm
from .utils import google_url_shorten, google_url_expand, keys_exists, create_period, create_period_detail, create_url


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
            
            # Retrieve the previous record
            url_record = Urls.objects.filter(input_url=input_url)

            # Previous record exists, delete record (Note cascade deletion not working)
            if url_record:
                url_to_delete = Urls.objects.get(input_url=input_url)
                url_to_delete.delete()

            # Create new record 
            # Create tiny url
            output_short = google_url_shorten(input_url)
            print("The response: %s" % output_short)

            # Verify response type (Successful url creation)
            if 'id' in output_short:
                short_url = output_short['id']
                print("Extracting the short url: %s" % short_url)

                # Successful tiny url creation, retrieve analytics data
                output_expand = google_url_expand(short_url)
                print("Printing the full url: %s" % output_expand)
                
                # Successful: Analytics call
                if 'created' in output_expand:
                    new_url = create_url(output_expand)
                # Unsuccesful: Error message
                else: 
                    test = 1
            return HttpResponseRedirect(reverse('shorterner:list')) # change to error page, invalid url
        return render(request, self.template_name, {'form': form})

class IndexView(generic.ListView):
    template_name = 'shorterner/list.html'
    context_object_name = 'url_list'

    def get_queryset(self):
        return Urls.objects.all()

class DetailView(generic.DetailView):
    template_name = "shorterner/detail.html"
    model = Urls
    slug_url_kwarg = 'slug'
    query_pk_and_slug = True
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context[''] = Urls.objects.filter(
    #         input_url=slug_url_kwarg
    #         ).filter(

    #         )
        # return context




