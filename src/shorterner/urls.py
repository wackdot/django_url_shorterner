from django.urls import path, re_path
from . import views

app_name = 'shorterner'

urlpatterns = [
    #path('', views.shorterner_index, name="input"),
    path('request/', views.RequestView.as_view(), name="request"),
    path('list/', views.IndexView.as_view(), name="list"),
    re_path('list/(?P<slug>[-\w]+)/$', views.DetailView.as_view(), name="details")
]