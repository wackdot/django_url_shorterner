from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.conf import settings
from django.urls import reverse
from django.views import View, generic
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.core import serializers
from django.http import Http404

from .models import ErrorDetail, Error, Period, PeriodDetail, Url
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
            url_record = Url.objects.filter(input_url=input_url)

            # Previous record exists, delete record (Note cascade deletion not working)
            if url_record:
                url_to_delete = Url.objects.get(input_url=input_url)
                url_to_delete.delete()
                print("deleted")

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
                    new_url = create_url(output_expand, input_url)
                # Unsuccesful: Error message
                else: 
                    test = 1
            return HttpResponseRedirect(reverse('shorterner:url-list'))
        return render(request, self.template_name, {'form': form})

class IndexView(generic.ListView):
    template_name = 'shorterner/list.html'
    context_object_name = 'url_list'

    def get_queryset(self):
        return Url.objects.all()

class DetailView(DetailView):
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
        alltime_referrer = PeriodDetail.objects.filter(pk=alltime.referrer.pk)

        context['alltime'] = self.object.alltime




        return context

# class UrlDetails(generic.ListView):
#     template_name = 'shorterner/detail.html'

#     def get(self, request, *args, **kwargs):
#         pk = self.kwargs.get('pk')
#         self.object = self.get_object(queryset=Urls.objects.filter(pk__iexact=pk))
#         return super.get(request, *args, **kwargs)
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['alltime_list'] = self.object.Urls_alltime=True

#         return context


