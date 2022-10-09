from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from main_app.forms import UserCreationForm, ProfileForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Artists, UserProfile
import requests
import environ
from .spotify import artist_topsongs

env = environ.Env()

# Create your views here.

BASE_URL = 'https://api.seatgeek.com/2/'

event = 'events'

performers = 'performers/'

postal_code = 'postal_code='

query = '?'

clientID_secret = env('SEATGEEK_CLIENTID_SECRET')




def call_api_with_filters_for_event(parameters):
    if parameters != 'placeholder':
        filter_concert_URL = BASE_URL + event + query + "type=concert&"
        filter_festival_URL = BASE_URL + event + query + "type=music_festival&"
        for key in parameters:
            filter_concert_URL = filter_concert_URL + key + '=' + parameters[key] + '&'
        
        for key in parameters:
            filter_festival_URL = filter_festival_URL + key + '=' + parameters[key] + '&'
    else: 
        filter_concert_URL = BASE_URL + event + query + "type=concert&" + clientID_secret
        filter_festival_URL = BASE_URL + event + query + "type=music_festival&" + clientID_secret
    filter_concert_URL = filter_concert_URL + clientID_secret
    filter_festival_URL = filter_festival_URL + clientID_secret
    concert_response = requests.get(filter_concert_URL)
    festival_response = requests.get(filter_festival_URL)
    concert_json = concert_response.json()
    festival_json = festival_response.json()
    return (concert_json, festival_json)


def call_api_for_artist_data(parameters):
    filter_artist_URL = BASE_URL + performers + str(parameters) + '?' + clientID_secret


    artist_response = requests.get(filter_artist_URL)
    
    artist_json = artist_response.json()
    return artist_json


def home(request):
    events = call_api_with_filters_for_event('placeholder')
    return render(request, 'home.html', {'page_name': 'Home', 'events':events[0], 'festivals':events[1]})


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

def artist_detail(request, artist_seatgeek_id):
    artist = call_api_for_artist_data(artist_seatgeek_id)
    artist_id=artist['links'][0]['id'][15:]
    topsongs = artist_topsongs(artist_id)
    return render(request, 'artists/artist_detail.html', {'artist':artist, 'artist_top_songs': topsongs})


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
def user_profile_edit(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user.profile)

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='user_profile')
    else:
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'main_app/userprofile_form.html', {'profile_form': profile_form, 'page_name': 'My Profile'})
    # user_profile = UserProfile.objects.get(id=request.user)
"""    return render(request, 'user_profile.html', { 'page_name': 'My Profile'})
"""

def user_profile(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'user_profile.html', {'profile': profile})

def follow_or_create_artist(request, seatgeek_id, user_id):
    if Artists.objects.filter(artist_seatgeek_id=seatgeek_id).exists():
        called_artist = Artists.objects.filter(artist_seatgeek_id=seatgeek_id)
        id = ''
        for artist in called_artist:
            id = artist.id
        UserProfile.objects.get(user=user_id).fav_artists.add(id)
    else:
        artist = call_api_for_artist_data(seatgeek_id)
        new_entry = Artists(
            artist=artist['name'], 
            artist_query=artist['name'].replace(" ", "-").lower(), 
            artist_spotify_uri=artist['links'][0]['id'][15:], 
            artist_seatgeek_id = seatgeek_id)
        new_entry.save()
        called_artist = Artists.objects.filter(artist_seatgeek_id=seatgeek_id)
        id = ''
        for artist in called_artist:
            id = artist.id
        UserProfile.objects.get(user=user_id).fav_artists.add(id)
    return redirect('user_profile')



def spotify(request):
    return render(request, 'spotify.html')
