from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from main_app.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserProfile
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
    return render(request, 'events/search.html', {'events':events, 'page_name': 'Events'})


def about(request):
    return render(request, 'about.html', {'page_name': 'About'})


def detail(request):
    return render(request, 'events/detail.html', {'page_name': 'Detail'})


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

