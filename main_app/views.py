from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import requests

# Create your views here.

BASE_URL = 'https://api.seatgeek.com/2/'

event = 'events'

postal_code = 'postal_code='

query = '?'

clientID_secret = 'client_id=OTc2OTUzNXwxNjY0NTk3NTY4LjUxNDAyNDc&client_secret=4cf673c06f28e56eee32b56e8841274e1e0e039e7559db50d787f8d887f24f4d'


def call_api_with_filters_for_event(parameters):
    filter_event_URL = BASE_URL + event + query + "type=concert&"
    for key in parameters:
        filter_event_URL = filter_event_URL + key + '=' + parameters[key] + '&'
    filter_event_URL = filter_event_URL + clientID_secret
    print(filter_event_URL)
    response = requests.get(filter_event_URL)
    json = response.json()
    return json


def home(request):
    return render(request, 'home.html', {'page_name': 'Home'})


def search(request):
    queries = request.GET.copy()
    for key in queries.copy():
        if queries[key] == "":
            del queries[key]
        elif key == "range":
            queries[key] = queries[key] + "mi"
        elif key == "performers.slug":
            queries[key] = queries[key].replace(" ", "-").lower()

    events = call_api_with_filters_for_event(queries)        
    return render(request, 'search.html', {'events':events})


def about(request):
    return render(request, 'about.html', {'page_name': 'About'})

