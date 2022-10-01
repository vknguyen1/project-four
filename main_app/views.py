from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import requests
# Create your views here.


BASE_URL = 'https://api.seatgeek.com/2/'

event = 'events'

postal_code = 'postal_code='

query = '?'

clientID_secret = '&client_id=OTc2OTUzNXwxNjY0NTk3NTY4LjUxNDAyNDc&client_secret=4cf673c06f28e56eee32b56e8841274e1e0e039e7559db50d787f8d887f24f4d'


def zipcodeFilter(zipcode):
    filterZipcodeURL = BASE_URL + event + query + postal_code + zipcode + clientID_secret
    response = requests.get(filterZipcodeURL)
    json = response.json()
    return json


def home (request):
    return render(request, 'home.html')


def search(request, zipcode):
    filteredEvent = zipcodeFilter(str(zipcode))
    return render(request, 'search.html', {'event' : filteredEvent})