from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('about/', views.about, name='about'),
    path('events/detail/', views.detail, name='detail'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('accounts/signup/', views.signup, name='signup')
]