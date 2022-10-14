
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic.edit import DeleteView
from main_app.forms import UserCreationForm, ProfileForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Artists, FollowedEvent, UserProfile
import requests
import environ
from .spotify import artist_topsongs, artist_related_artists
from datetime import datetime

env = environ.Env()

# Create your views here.
# TO-DO @login_required and loginrequiredmixin to necessary views


## Declared static variables that can be used across multiple different functions, probably could be kept in a .env file just like the secrets

BASE_URL = 'https://api.seatgeek.com/2/'

event = 'events'

performers = 'performers/'

postal_code = 'postal_code='

recommendations = 'recommendations/performers?performers.id='

query = '?'

clientID_secret = env('SEATGEEK_CLIENTID_SECRET')

## function to call api to look up events with filters

def call_api_with_filters_for_event(parameters):

    ## parameters are pushed through
    if parameters != 'placeholder':

    ## seatgeek stores concert and music festival separately, thus 2 calls, 1 for each
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
    ## returns both calls into a list, with each call being an entry in the list
    return (concert_json, festival_json)


## function to call artist data

def call_api_for_artist_data(parameters):
    filter_artist_URL = BASE_URL + performers + str(parameters) + query + clientID_secret

    artist_response = requests.get(filter_artist_URL)
    
    artist_json = artist_response.json()
    return artist_json

## function to call specific event data
def call_api_for_event_data(parameters):
    filter_event_URL = BASE_URL + event + '/' + str(parameters) + query + clientID_secret

    event_response = requests.get(filter_event_URL)     

    event_json = event_response.json() 
    return event_json

## function to call related artists
def call_similar_performers(performers):
    filter_performer_URL = BASE_URL + recommendations + str(performers) + '&' + clientID_secret
    
    performer_response = requests.get(filter_performer_URL)

    response_json = performer_response.json()

    return response_json

def home(request):
    events = call_api_with_filters_for_event('placeholder')
    return render(request, 'home.html', {'page_name': 'Home', 'events':events[0], 'festivals':events[1]})

## for search html
def search(request):
## search html is accessed by submitting a form at home page, queries gets the query params that are typed in that form (queries are received as a dictionary)
    queries = request.GET.copy()
    postal_code = ""
    range = ""
    performers = ""
    ## loops through dictionary, removes queries with an empty string for value, assigns filled queries to variables to be passed to the event api call function
    for key in queries.copy():
        if queries[key] == "":
            del queries[key]
        elif key == "postal_code":
            postal_code = queries[key]
        elif key == "range":
            queries[key] = queries[key] + "mi"
            range = queries[key]
        elif key == "performers.slug":
            queries[key] = queries[key].replace(" ", "-").lower()
            performers = queries[key]
    ## calls api for list of events that fits the queries, passing the queries as parameter (remember that the function returns 2 things, 1 for concert and 1 for festival)
    events = call_api_with_filters_for_event(queries)     
    return render(request, 'events/search.html', {'events':events[0], 'festivals':events[1], 'postal_code': postal_code, 'range':range, 'performers': performers, 'page_name': 'Events'})


def about(request):
    return render(request, 'about.html', {'page_name': 'About'})

## event details
def detail(request, event_id):
    profile = ''
    event_entries = ''
    if request.user.is_authenticated:
        ## assigns the user profile of currently logged in user to profile variable
        profile = UserProfile.objects.get(user=request.user)
        ## filters a user profile that is assigned to the currently logged in user, and returns data as a tuple. flat=true returns single values, which works since the data is only from 1 field
        event_entries = UserProfile.objects.filter(user=request.user).values_list('followed_event__event_seatgeek_id', flat = True)
    event = call_api_for_event_data(event_id)    
    return render(request, 'events/detail.html', {'page_name': 'Detail', 'event': event, 'profile':profile, 'event_entries': event_entries})


def artist_detail(request, artist_seatgeek_id):
    profile = ''
    artist_entries = ''
    ## same thing like event detail but for artist
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        artist_entries = UserProfile.objects.filter(user=request.user).values_list('fav_artists__artist_seatgeek_id', flat = True)
    artist = call_api_for_artist_data(artist_seatgeek_id)
    related_artist = call_similar_performers(artist_seatgeek_id)
    topsongs = ""
    performer_id = {'performers.id':str(artist_seatgeek_id)}
    artist_upcoming_events = call_api_with_filters_for_event(performer_id)

    ## if artist has links in the seatgeek api data, it'll be used to look up spotify data
    if artist['links']:
        artist_id=artist['links'][0]['id'][15:]
        topsongs = artist_topsongs(artist_id)
        

    return render(request, 'artists/artist_detail.html', {
        'artist':artist, 
        'artist_top_songs': topsongs, 
        'profile': profile, 
        'artist_related_artists': related_artist,
        'artist_entries': artist_entries,
        'artist_upcoming_concerts': artist_upcoming_events[0],
        'artist_upcoming_festivals': artist_upcoming_events[1],
        })


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


def user_profile(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'user_profile.html', {'profile': profile})


## many to many relationship (for following an artist)
def follow_or_create_artist(request, seatgeek_id, user_id):

    ## if artist is already in the database, just form relationship
    if Artists.objects.filter(artist_seatgeek_id=seatgeek_id).exists():
        called_artist = Artists.objects.filter(artist_seatgeek_id=seatgeek_id)
        id = ''
        for artist in called_artist:
            id = artist.id
        UserProfile.objects.get(user=user_id).fav_artists.add(id)
    ## otherwise, create artist in database first then form relationship
    else:
        artist = call_api_for_artist_data(seatgeek_id) ## get artist data from seatgeek api
        if artist['links']: ## add spotify uri if it exists, otherwise, no spotify uri field. the following fields are filled with the data based on the data given from the api
            new_entry = Artists(
                artist=artist['name'], 
                artist_query=artist['name'].replace(" ", "-").lower(), 
                artist_spotify_uri=artist['links'][0]['id'][15:], 
                artist_seatgeek_id = seatgeek_id,
                artist_image=artist['image'])
        else:
            new_entry = Artists(
                artist=artist['name'], 
                artist_query=artist['name'].replace(" ", "-").lower(), 
                artist_seatgeek_id = seatgeek_id,
                artist_image=artist['image'])
        new_entry.save()
        called_artist = Artists.objects.filter(artist_seatgeek_id=seatgeek_id)
        id = ''
        for artist in called_artist:
            id = artist.id
        UserProfile.objects.get(user=user_id).fav_artists.add(id)
    return redirect('artist_detail', seatgeek_id)


## unfollow artist
def unfollow_artist(request, seatgeek_id, user_id):
    called_artist = Artists.objects.filter(artist_seatgeek_id=seatgeek_id)
    id = ''
    for artist in called_artist:
        id = artist.id
    UserProfile.objects.get(user=user_id).fav_artists.remove(id)
    return redirect('artist_detail', seatgeek_id)


## same thing like artist, but for event.
def follow_or_create_event(request, event_id, user_id):
    if FollowedEvent.objects.filter(event_seatgeek_id=event_id).exists():
        called_event = FollowedEvent.objects.filter(event_seatgeek_id=event_id)
        id = ''
        for event in called_event:
            id = event.id
        UserProfile.objects.get(user=user_id).followed_event.add(id)
    else:
        event = call_api_for_event_data(event_id)        
        new_entry = FollowedEvent(
            event_name=event['title'], 
            event_date=datetime.strptime(event['datetime_local'], '%Y-%m-%dT%H:%M:%S'), 
            event_seatgeek_id = event_id,
            event_image=event['performers'][0]['image'])
        new_entry.save()
        called_event = FollowedEvent.objects.filter(event_seatgeek_id=event_id)
        id = ''
        for specificevent in called_event:
            id = specificevent.id
        UserProfile.objects.get(user=user_id).followed_event.add(id)
        for performers in event['performers']:                              ##filters performers in event, then add performers relationship to event if performer already exists, otherwise create new database entry for the performers
            artist = call_api_for_artist_data(performers['id']) 
            if artist['links']: 
                new_entry = Artists(
                    artist=artist['name'], 
                    artist_query=artist['name'].replace(" ", "-").lower(), 
                    artist_spotify_uri=artist['links'][0]['id'][15:], 
                    artist_seatgeek_id = performers['id'],
                    artist_image=artist['image'])
            else:
                new_entry = Artists(
                    artist=artist['name'], 
                    artist_query=artist['name'].replace(" ", "-").lower(), 
                    artist_seatgeek_id = performers['id'],
                    artist_image=artist['image'])
            new_entry.save()
            called_artist = Artists.objects.filter(artist_seatgeek_id=performers['id'])
            id = ''
            for artist in called_artist:
                id = artist.id
            FollowedEvent.objects.get(event_seatgeek_id=event_id).event_artist.add(id)
    return redirect('detail', event_id)


def unfollow_event(request, event_id, user_id):
    called_event = FollowedEvent.objects.filter(event_seatgeek_id=event_id)
    id = ''
    for event in called_event:
        id = event.id
    UserProfile.objects.get(user=user_id).followed_event.remove(id)
    return redirect('detail', event_id)


def spotify(request):
    return render(request, 'spotify.html')


## simple user deletion
class UserDeleteView(DeleteView):
    model = User
    success_url = '/'