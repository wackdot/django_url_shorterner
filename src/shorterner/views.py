from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.conf import settings
from django.urls import reverse, reverse_lazy
from django.views import View, generic
from django.core import serializers
from django.http import Http404

from .models import Error, Period, PeriodDetail, Url
from .forms import SubmitUrlForm
from .utils import google_url_shorten, google_url_expand, keys_exists, create_period, create_period_detail, create_url, create_analytics, create_error

invalid_email = 'https://portal.wdf.sap.corp/irj/go/km/docs/guid/600840f6-2d2d-2e10-5bb7-##fca7779a24cc'

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
            url_record = Url.objects.filter(input_url=input_url)

            # Previous record exists, delete record (Note cascade deletion not working)
            if url_record:
                url_record.delete()
                print("Deleted")

            # Create new record 
            # Create tiny url
            output_short = google_url_shorten(input_url)
            print("The response: %s" % output_short)

            # Successful: Url creation
            if 'id' in output_short:
                print("Successful url creation")
                short_url = output_short['id']

                # Successful tiny url creation, retrieve analytics data
                output_expand = google_url_expand(short_url)
                print("Printing the full url: %s" % output_expand)
                
                # Generate url + analytics
                new_url = create_url('Success', input_url, create_analytics(output_expand), output_expand)
                print("Url Details + Analytics created!")
            # Unsuccesful: Error message
            else: 
                print("Unsuccessful url creation")
                # Generate url + error message
                new_url = create_url('Unsuccessful', input_url, create_error(output_short))
                print("Url Details + Error Message created!")
            return HttpResponseRedirect(reverse('shorterner:url-list'))
        return render(request, self.template_name, {'form': form})

class IndexView(generic.ListView):
    template_name = 'shorterner/list.html'
    context_object_name = 'url_list'

    def get_queryset(self):
        return Url.objects.all()

class DetailView(generic.DetailView):
    template_name = 'shorterner/detail.html'
    context_object_name = 'url_details'

    def get_object(self):
        pk = self.kwargs.get("pk")
        if pk is None:
            raise Http404
        return get_object_or_404(Url, pk__iexact=pk)

    def get_context_data(self, **kwargs):
        # Calls the base implementation first to get a context
        context = super(DetailView, self).get_context_data(**kwargs)
        alltime = self.object.alltime
        month = self.object.month
        week = self.object.week
        day = self.object.day
        twohour = self.object.twohour
        errormessage = self.object.errormessage

        # Check if object short url is blank
        if alltime is not None:
            alltime_referrer = alltime.referrer.all() 
            alltime_country = alltime.country.all()
            alltime_browser = alltime.browser.all()
            alltime_platform = alltime.platform.all()  

            context['alltime'] = alltime
            context['alltime_referrer'] = alltime_referrer
            context['alltime_country'] = alltime_country
            context['alltime_browser'] = alltime_browser
            context['alltime_platform'] = alltime_platform

        if month is not None:
            month_referrer = month.referrer.all() 
            month_country = month.country.all()
            month_browser = month.browser.all()
            month_platform = month.platform.all()  

            context['month'] = month
            context['month_referrer'] = month_referrer
            context['month_country'] = month_country
            context['month_browser'] = month_browser
            context['month_platform'] = month_platform
        if week is not None:
            week_referrer = week.referrer.all() 
            week_country = week.country.all()
            week_browser = week.browser.all()
            week_platform = week.platform.all()  

            context['week'] = week
            context['week_referrer'] = week_referrer
            context['week_country'] = week_country
            context['week_browser'] = week_browser
            context['week_platform'] = week_platform
        if day is not None:
            day_referrer = day.referrer.all() 
            day_country = day.country.all()
            day_browser = day.browser.all()
            day_platform = day.platform.all()  

            context['day'] = day
            context['day_referrer'] = day_referrer
            context['day_country'] = day_country
            context['day_browser'] = day_browser
            context['day_platform'] = day_platform 
        if twohour is not None:
            twohour_referrer = twohour.referrer.all() 
            twohour_country = twohour.country.all()
            twohour_browser = twohour.browser.all()
            twohour_platform = twohour.platform.all()  

            context['twohour'] = twohour
            context['twohour_referrer'] = twohour_referrer
            context['twohour_country'] = twohour_country
            context['twohour_browser'] = twohour_browser
            context['twohour_platform'] = twohour_platform
        if errormessage is not None:
            context['errormessage'] = errormessage
        return context
    
class DeleteView(generic.DeleteView):
    model = Url
    success_url = reverse_lazy("shorterner:url-list")
    template_name = "shorterner/delete.html"



