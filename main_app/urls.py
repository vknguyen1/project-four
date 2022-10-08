from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('about/', views.about, name='about'),
    path('events/detail/', views.detail, name='detail'),
    path('artists/detail/<int:artist_seatgeek_id>', views.artist_detail, name='artist_detail'),
    path('artists/<int:seatgeek_id>/assignuser/<int:user_id>', views.follow_or_create_artist, name='follow_or_create_artist'), 
    path('user_profile/', views.user_profile, name='user_profile'),
    path('accounts/signup/', views.signup, name='signup')
]