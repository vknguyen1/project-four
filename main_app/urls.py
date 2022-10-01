from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/<int:zipcode>', views.search, name='actual-search'),
    path('search/', views.search, name='search')
]