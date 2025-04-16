"""
Contains paths relating to URLs of home app.

The path function defines URL patterns in Django.
The views file implements index and about functions that render a welcome message and
    about page respectively.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home.index'),
    path('about/', views.about, name='home.about'),
]