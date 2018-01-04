from django.urls import path
from . import views

app_name = 'shorterner'

urlpatterns = [
    #path('', views.shorterner_index, name="input"),
    path('request/', views.RequestView.as_view(), name="url-request"),
    path('list/', views.IndexView.as_view(), name="url-list"),
    path('<slug:slug>/', views.DetailView.as_view(), name="url-detail")
]