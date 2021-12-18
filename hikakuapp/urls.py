from django.urls import path
from . import views

app_name = 'hikaku'

urlpatterns = [
    path('', views.SearchView.as_view(), name = 'index'),
]
