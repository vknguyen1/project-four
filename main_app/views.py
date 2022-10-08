from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from main_app.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserProfile
import requests
import environ

env = environ.Env()

# Create your views here.

BASE_URL = 'https://api.seatgeek.com/2/'

event = 'events'

performers = 'performers/'

postal_code = 'postal_code='

query = '?'

clientID_secret = env('clientID_secret')


def call_api_with_filters_for_event(parameters):
    filter_concert_URL = BASE_URL + event + query + "type=concert&"
    filter_festival_URL = BASE_URL + event + query + "type=music_festival&"
    for key in parameters:
        filter_concert_URL = filter_concert_URL + key + '=' + parameters[key] + '&'
    filter_concert_URL = filter_concert_URL + clientID_secret
    for key in parameters:
        filter_festival_URL = filter_festival_URL + key + '=' + parameters[key] + '&'
    filter_festival_URL = filter_festival_URL + clientID_secret
    concert_response = requests.get(filter_concert_URL)
    festival_response = requests.get(filter_festival_URL)
    concert_json = concert_response.json()
    festival_json = festival_response.json()
    return (concert_json, festival_json)


def call_api_for_artist_data(parameters):
    filter_artist_URL = BASE_URL + performers 
    for key in parameters:
        filter_artist_URL = filter_artist_URL + parameters[key] + '?' + clientID_secret
    print (filter_artist_URL)
    artist_response = requests.get(filter_artist_URL)
    
    artist_json = artist_response.json()
    return artist_json


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
    return render(request, 'events/search.html', {'events':events[0], 'festivals':events[1], 'page_name': 'Events'})


def about(request):
    return render(request, 'about.html', {'page_name': 'About'})


def detail(request):
    return render(request, 'events/detail.html', {'page_name': 'Detail'})

def artist_detail(request):
    queries = request.GET.copy()
    artist = call_api_for_artist_data(queries)
    return render(request, 'artists/artist_detail.html', {'artist':artist})


def signup(request):
    form = UserCreationForm()
    error_message = ''

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user_profile')
        else:
            error_message = 'invalid credentials'

    context = {'form': form, 'error_message': error_message}

    return render(request, 'registration/signup.html', context)

# TO-DO @login_required
def user_profile(request):
    # user_profile = UserProfile.objects.get(id=request.user)
    return render(request, 'user_profile.html', { 'page_name': 'My Profile'})

# TO-DO Add LoginRequiredMixin
# class UserProfileCreate(CreateView): 
#     model = UserProfile
#     fields = '__all__'

