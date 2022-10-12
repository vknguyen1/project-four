from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('about/', views.about, name='about'),
    path('events/detail/<int:event_id>', views.detail, name='detail'),
    path('artists/detail/', views.artist_detail, name='artist_detail'),
    path('artists/detail/<int:artist_seatgeek_id>', views.artist_detail, name='artist_detail'),
    path('artists/<int:seatgeek_id>/assignuser/<int:user_id>', views.follow_or_create_artist, name='follow_or_create_artist'),
    path('artists/<int:seatgeek_id>/unassignuser/<int:user_id>', views.unfollow_artist, name='unfollow_artist'),
    path('events/<int:event_id>/assignuser/<int:user_id>', views.follow_or_create_event, name='follow_or_create_event'),
    path('events/<int:event_id>/unassignuser/<int:user_id>', views.unfollow_event, name='unfollow_event'),  
    path('user_profile/', views.user_profile, name='user_profile'),
    path('user_profile/edit/', views.user_profile_edit, name='user_profile_edit'),
    path('accounts/signup/', views.signup, name='signup'),
    path('spotify/', views.spotify, name='spotify'),

]