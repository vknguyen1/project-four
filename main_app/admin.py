from django.contrib import admin
from .models import UserProfile, FollowedEvent, Zipcodes, Artists, Genre, Playlist

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(FollowedEvent)
admin.site.register(Zipcodes)
admin.site.register(Artists)
admin.site.register(Genre)
admin.site.register(Playlist)