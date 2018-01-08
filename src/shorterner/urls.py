from django.urls import path
from . import views

app_name = 'shorterner'

urlpatterns = [
    path('request/', views.RequestView.as_view(), name="url-request"),
    path('list/', views.IndexView.as_view(), name="url-list"),
    path('<int:pk>/', views.DetailView.as_view(), name="url-detail"),
    path('delete/<int:pk>/', views.DeleteView.as_view(), name="url-delete")
]