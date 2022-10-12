from enum import unique
from unittest.util import _MAX_LENGTH
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Genre(models.Model):
    genre = models.CharField(max_length=20)

    def __str__(self):
        return self.genre

class Artists(models.Model):
    artist = models.CharField(max_length=50)
    artist_query = models.CharField(max_length=50)
    artist_genre = models.ManyToManyField(Genre)
    artist_spotify_uri = models.CharField(max_length=100)
    artist_seatgeek_id = models.IntegerField(unique)
    artist_image = models.CharField(max_length=200)
    
    def __str__(self):
        return self.artist

class Playlist(models.Model):
    spotify_playlist_link = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class FollowedEvent(models.Model):
    event_name = models.CharField(max_length=50)
    event_date = models.DateField()
    event_seatgeek_id = models.IntegerField(unique)
    event_image = models.CharField(max_length=200)

    def __str__(self):
        return self.event_name

    class Meta:
        ordering = ['event_date'] # or ['-event_date'] for decending order

class Zipcodes(models.Model):
    zipcode = models.CharField(max_length=10)

    def __str__(self):
        return self.zipcode  # not sure if this is neessary here or if we should change the field to Integer

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,  related_name='profile')
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    fav_artists = models.ManyToManyField(Artists)
    fav_genre = models.ManyToManyField(Genre)
    followed_playlist = models.ManyToManyField(Playlist)
    followed_event = models.ManyToManyField(FollowedEvent)
    followed_zipcode = models.ManyToManyField(Zipcodes)

    def __str__(self):
        return self.first_name

